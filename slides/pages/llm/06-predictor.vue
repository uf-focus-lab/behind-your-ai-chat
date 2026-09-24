<script setup lang="ts">
// All a language model does: a distribution over the next token, take one,
// append, run again. Six real steps of the small model's reply to our
// message; each click appends the token it took and shows what it wanted
// next.
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import Stage from '../../components/Stage.vue'
import TokenStream, { type Chip } from '../../components/TokenStream.vue'
import data from '../../assets/llm/steps.json'

const { $clicks } = useSlideContext()
const step = computed(() => Math.min($clicks.value, data.steps.length - 1))
const top = computed(() => data.steps[step.value].top)
const show = (t: string) => (t.trim() === '' ? '␣' : t.replace(/^ /, '·'))

// the user's tokens, the agent marker, then one accent chip per token taken
const chips = computed<Chip[]>(() => [
  { key: 'mark-s', kind: 'mark', text: '[system]' },
  { key: 'sys', kind: 'tok', text: '…', tone: 'dim' },
  { key: 'mark-u', kind: 'mark', text: '[user]' },
  ...data.prefix[1].tokens.map((t, i) => ({ key: `u-${i}`, kind: 'tok' as const, text: t.token.trim() || '␣', id: t.id })),
  { key: 'mark-a', kind: 'mark', text: '[agent]' },
  ...data.steps.slice(0, step.value).map((s, i) => ({ key: `a-${i}`, kind: 'tok' as const, text: show(s.taken.token), id: s.taken.id, tone: 'accent' as const })),
])
</script>

<template>
  <Stage gap="1.8rem">
    <TokenStream :chips="chips" class="llm-pred-stream" />
    <div class="llm-pred">
      <p class="llm-pred-head">p(next token) over all 49 152 pieces, top five</p>
      <TransitionGroup tag="ul" name="llm-pred" class="llm-pred-bars">
        <li v-for="(t, i) in top" :key="`${step}-${t.id}`" :class="{ taken: i === 0 }">
          <span class="llm-pred-tok">{{ show(t.token) }}</span>
          <span class="llm-pred-bar"><i :style="{ width: `${t.p * 100}%` }" /></span>
          <span class="llm-pred-p">{{ t.p.toFixed(2) }}</span>
        </li>
      </TransitionGroup>
    </div>
  </Stage>
</template>

<style scoped>
.llm-pred-stream { --ts-size: 20px; --ts-id-size: 12px; --ts-pad: 5px 9px 3px; --ts-gap: 8px 6px; --ts-mark-size: 18px; --ts-mark-pad: 8px 10px; }
.llm-pred { width: 560px; display: flex; flex-direction: column; gap: 0.5rem; }
p.llm-pred-head { margin: 0; font-size: 18px; color: var(--ink-faint); text-align: center; }
.llm-pred-bars { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 5px; position: relative; }
.llm-pred-bars li { display: grid; grid-template-columns: 110px 1fr 56px; align-items: center; gap: 12px; margin: 0; }
.llm-pred-tok { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 21px; color: var(--ink-strong); text-align: right; white-space: pre; }
.llm-pred-bar { height: 16px; background: var(--ink-hair); }
.llm-pred-bar i { display: block; height: 100%; background: var(--ink); transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
li.taken .llm-pred-bar i { background: var(--accent); }
li.taken .llm-pred-tok { color: var(--accent); }
.llm-pred-p { font-size: 18px; color: var(--ink); font-variant-numeric: tabular-nums; }
.llm-pred-enter-active { transition: opacity 0.4s ease 0.2s; }
.llm-pred-leave-active { transition: opacity 0.2s ease; position: absolute; width: 100%; }
.llm-pred-enter-from, .llm-pred-leave-to { opacity: 0; }
</style>
