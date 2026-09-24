<script setup lang="ts">
// A real tool turn as the model reads it, in three clicks: the stream the
// program sent, with the tool schema in it; the call the model wrote; the
// result the program appended; the reply. Same chips as the hello-world
// stream, because it is the same thing.
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import Stage from '../../components/Stage.vue'
import TokenStream, { type Chip } from '../../components/TokenStream.vue'
import data from '../../assets/llm/stream-tools.json'

const { $clicks } = useSlideContext()
const marker: Record<string, string> = { system: '[system]', tools: '[tools]', user: '[user]', call: '[agent]', tool: '[tool]', assistant: '[agent]' }
const tone: Record<string, Chip['tone'] | undefined> = { call: 'accent', tool: 'accent' }
// the first three parts are what the program sent; each click appends one more
const visible = computed(() => data.stream.slice(0, 3 + $clicks.value))

const chips = computed<Chip[]>(() =>
  visible.value.flatMap((m, r) => [
    { key: `mark-${r}`, kind: 'mark' as const, text: marker[m.role] },
    ...m.tokens.map((t, i) => ({ key: `${r}-${i}`, kind: 'tok' as const, text: t.token.trim() || '␣', id: t.id, tone: tone[m.role] })),
  ]),
)
</script>

<template>
  <Stage>
    <TokenStream :chips="chips" class="llm-every" />
  </Stage>
</template>

<style scoped>
.llm-every { --ts-size: 20px; --ts-id-size: 12px; --ts-pad: 5px 9px 3px; --ts-gap: 8px 6px; --ts-mark-size: 18px; --ts-mark-pad: 8px 10px; }
</style>
