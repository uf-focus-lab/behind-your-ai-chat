<script setup lang="ts">
// The frame every content page sits in. It takes the whole band under the
// slide title and centres its content in it, so every slide in the deck has
// the same vertical rhythm and none hangs in the top half.
//
//   <Stage> ...one visual... </Stage>
//   <Stage row gap="2.5rem"> ...side by side... </Stage>
//
// The band is 866 by 415 slide px under a one-line title. Size the visual to
// use it. Do not add padding-top to push content down; the Stage centres it. Variables on the element: --stage-h (default 415px),
// --stage-gap.
defineProps<{ row?: boolean; gap?: string }>()
</script>

<template>
  <div class="deck-stage" :class="{ row }" :style="gap ? { '--stage-gap': gap } : undefined">
    <slot />
  </div>
</template>

<style scoped>
.deck-stage {
  height: var(--stage-h, 415px);
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--stage-gap, 1.2rem);
  min-height: 0;
}
.deck-stage.row {
  flex-direction: row;
}
</style>
