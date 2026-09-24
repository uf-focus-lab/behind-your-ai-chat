<script setup lang="ts">
// A terminal card with a live cursor: the mark of a slide that hands the
// room over to a demo. Fixed dark colours in both schemes, the same ones the
// agents slide draws.
//
//   <Terminal cmd="python chat.py" />
withDefaults(defineProps<{ cmd: string; width?: string }>(), { width: '520px' })
</script>

<template>
  <div class="term" :style="{ width }">
    <span class="term-lights" aria-hidden="true"><i /><i /><i /></span>
    <p class="term-cmd"><span class="term-prompt">$</span> {{ cmd }}<span class="term-cursor" aria-hidden="true" /></p>
  </div>
</template>

<style scoped>
.term {
  position: relative;
  padding: 2.1rem 1.6rem 1.4rem;
  border-radius: 12px;
  background: #1b1e23;
  border: 1px solid #3a3f47;
  box-shadow: 0 18px 48px -12px rgba(0, 0, 0, 0.45);
}
.term-lights { position: absolute; top: 12px; left: 14px; display: flex; gap: 7px; }
.term-lights i { width: 10px; height: 10px; border-radius: 50%; background: #3a3f47; }
p.term-cmd { margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 28px; line-height: 1.3; color: #ececec; white-space: nowrap; }
.term-prompt { color: #5bb3ff; margin-right: 0.3em; }
.term-cursor {
  display: inline-block;
  width: 0.6em; height: 1.1em;
  margin-left: 0.25em;
  vertical-align: -0.2em;
  background: #ececec;
  animation: term-blink 1.1s steps(1) infinite;
}
@keyframes term-blink { 50% { opacity: 0; } }
</style>
