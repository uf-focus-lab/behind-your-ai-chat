<script setup lang="ts">
// A conversation as the model reads it: one wrapped row of token chips, a
// marker chip where each role begins. Used by every "stream" slide so they
// all speak the same visual language.
//
//   <TokenStream :chips="chips" />               boxes on
//   <TokenStream :chips="chips" :boxed="false" /> bare words, boxes come later
//
// A chip is { key, kind: 'mark' | 'tok' | 'typing', text?, id?, vt?, delay?,
// tone? }. `vt` is a view-transition-name, `delay` the wait before this
// chip's box and id draw once `boxed` turns on, `tone` colours the chip.
// Chips inserted or removed by a click fade, and the rest slide to make room.
export type Chip = {
  key: string
  kind: 'mark' | 'tok' | 'typing' | 'img'
  text?: string
  id?: number
  vt?: string
  delay?: string
  tone?: 'accent' | 'dim'
  /** for an 'img' chip: the tile's background, position and size */
  tile?: Record<string, string>
}
withDefaults(defineProps<{ chips: Chip[]; boxed?: boolean }>(), { boxed: true })
</script>

<template>
  <TransitionGroup tag="div" name="ts" class="ts" :class="{ boxed }">
    <span v-for="c in chips" :key="c.key" class="ts-chip" :class="[`is-${c.kind}`, c.tone && `tone-${c.tone}`]" :style="{ viewTransitionName: c.vt, '--d': c.delay ?? '0s' }">
      <template v-if="c.kind === 'tok'"><span class="ts-tok">{{ c.text }}</span><span class="ts-id">{{ c.id }}</span></template>
      <template v-else-if="c.kind === 'mark'">{{ c.text }}</template>
      <template v-else-if="c.kind === 'img'"><span class="ts-tile" :style="c.tile" /></template>
      <template v-else><i /><i /><i /></template>
    </span>
  </TransitionGroup>
</template>

<style scoped>
.ts {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: center;
  gap: var(--ts-gap, 10px 8px);
  max-width: var(--ts-w, 866px);
}
.ts-chip {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: var(--ts-pad, 6px 11px 4px);
  border: 1.5px solid transparent;
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  transition: border-color 0.45s ease;
}
.ts-tok { font-size: var(--ts-size, 23px); line-height: 1.2; color: var(--ink-strong); white-space: pre; }
.ts-id { font-size: var(--ts-id-size, 14px); line-height: 1.2; color: var(--ink-faint); opacity: 0; transition: opacity 0.45s ease; }
/* Boxes write in at the token pace; they fade out together, no delay. */
.boxed .is-tok { border-color: color-mix(in srgb, var(--ink-strong) 38%, transparent); transition-delay: var(--d); }
.boxed .is-tok .ts-id { opacity: 1; transition-delay: var(--d); }
.boxed .is-tok.tone-accent { border-color: color-mix(in srgb, var(--accent) 70%, transparent); }
.tone-accent .ts-tok { color: var(--accent); }
.boxed .is-tok.tone-dim { border-color: color-mix(in srgb, var(--ink-strong) 18%, transparent); }
.tone-dim .ts-tok { color: var(--ink-dim); }
.is-img { padding: 3px; }
.boxed .is-img { border-color: color-mix(in srgb, var(--ink-strong) 38%, transparent); transition-delay: var(--d); }
.boxed .is-img.tone-accent { border-color: color-mix(in srgb, var(--accent) 70%, transparent); }
.ts-tile { display: block; width: var(--ts-tile, 40px); height: var(--ts-tile, 40px); background-size: var(--ts-tile-bg); background-repeat: no-repeat; border-radius: 3px; }
.is-mark {
  padding: var(--ts-mark-pad, 9px 12px);
  border-color: color-mix(in srgb, var(--accent) 70%, transparent);
  color: var(--accent);
  font-size: var(--ts-mark-size, 21px);
  align-self: stretch;
  justify-content: center;
}
.is-typing { flex-direction: row; gap: 6px; padding: 16px 12px; border-style: dashed; border-color: var(--ink-dim); }
.is-typing i { width: 8px; height: 8px; border-radius: 50%; background: var(--ink-dim); }

/* Clicks insert chips: newcomers fade in, the rest slide to make room. These
   come last so they beat the boxed delay while a chip is in flight. */
.ts .ts-move,
.ts .ts-enter-active {
  transition: transform 0.55s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.45s ease, border-color 0.45s ease;
  transition-delay: 0s;
}
.ts .ts-leave-active { transition: opacity 0.25s ease; position: absolute; }
.ts-enter-from,
.ts-leave-to { opacity: 0; }
</style>
