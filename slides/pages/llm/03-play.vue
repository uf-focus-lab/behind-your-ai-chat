<script setup lang="ts">
// The cue to leave the deck for the terminal. Unlike the question slides,
// which are black serif, this one is an accent line over a terminal card
// with a live cursor, so the shape of the slide says "demo" before the
// words do. The line and the command are props, so the same page marks
// each visit.
//
//   <Play />                                          "Time to play", chat.py
//   <Play line="Back to the terminal" cmd="@tool" />
import Terminal from '../../components/Terminal.vue'
withDefaults(defineProps<{ line?: string; cmd?: string }>(), {
  line: 'Time to play',
  cmd: 'python chat.py',
})
</script>

<template>
  <div class="llm-play">
    <p class="llm-play-line">{{ line }}</p>
    <Terminal :cmd="cmd" />
  </div>
</template>

<style scoped>
.llm-play { height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2rem; }
p.llm-play-line { margin: 0; font-size: 56px; line-height: 1.1; font-weight: 600; color: var(--accent); }
</style>
