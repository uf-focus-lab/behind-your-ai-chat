<script setup lang="ts">
// Six illumination patterns a projector can throw, each animated the way the
// lab would step it, for inspiration: the separation needs a pattern with
// lit and unlit pixels close together, shifted so every pixel sees both.
import Stage from '../../components/Stage.vue'

const patterns = [
  { cls: 'checker', name: 'shifted checkerboard' },
  { cls: 'stripes-v', name: 'vertical stripes, phase-stepped' },
  { cls: 'stripes-h', name: 'horizontal stripes, sliding' },
  { cls: 'sine', name: 'sinusoid, phase-shifted' },
  { cls: 'dots', name: 'dot lattice, shifted' },
  { cls: 'sweep', name: 'one bright line, swept' },
]
</script>

<template>
  <Stage>
    <div class="lab-pat-grid">
      <figure v-for="p in patterns" :key="p.cls" class="lab-pat">
        <div class="lab-pat-screen" :class="p.cls" />
        <figcaption>{{ p.name }}</figcaption>
      </figure>
    </div>
  </Stage>
</template>

<style scoped>
.lab-pat-grid { display: grid; grid-template-columns: repeat(3, 264px); gap: 1.2rem 1.4rem; }
.lab-pat { margin: 0; display: flex; flex-direction: column; gap: 0.4rem; }
.lab-pat figcaption { font-size: 16px; color: var(--ink-faint); text-align: center; }
/* every screen is a dark projector frame; the pattern is what it throws */
.lab-pat-screen { width: 264px; height: 148px; border-radius: 6px; background-color: #0e0e10; box-shadow: inset 0 0 0 1px #2a2a2e; }

.checker {
  --c: 24px;
  background-image: repeating-conic-gradient(#f4f4f0 0 25%, #0e0e10 0 50%);
  background-size: calc(2 * var(--c)) calc(2 * var(--c));
  animation: lab-shift-x 1.6s steps(2, jump-none) infinite;
}
.stripes-v {
  background-image: repeating-linear-gradient(90deg, #f4f4f0 0 16px, #0e0e10 16px 48px);
  background-size: 48px 100%;
  animation: lab-shift-3 1.8s steps(3, jump-none) infinite;
}
.stripes-h {
  background-image: repeating-linear-gradient(180deg, #f4f4f0 0 14px, #0e0e10 14px 36px);
  background-size: 100% 36px;
  animation: lab-slide-y 2s linear infinite;
}
.sine {
  background-image: linear-gradient(90deg, #0e0e10, #f4f4f0 50%, #0e0e10);
  background-size: 64px 100%;
  animation: lab-slide-x 2.4s linear infinite;
}
.dots {
  background-image: radial-gradient(circle, #f4f4f0 6px, transparent 7px);
  background-size: 32px 32px;
  animation: lab-shift-dots 2s steps(4, jump-none) infinite;
}
.sweep {
  background-image: linear-gradient(90deg, transparent 0, #f4f4f0 0 12px, transparent 12px);
  background-size: 100% 100%;
  background-repeat: no-repeat;
  animation: lab-sweep 2.2s linear infinite;
}

@keyframes lab-shift-x { from { background-position: 0 0; } to { background-position: var(--c) 0; } }
@keyframes lab-shift-3 { from { background-position: 0 0; } to { background-position: 32px 0; } }
@keyframes lab-slide-y { from { background-position: 0 0; } to { background-position: 0 36px; } }
@keyframes lab-slide-x { from { background-position: 0 0; } to { background-position: 64px 0; } }
@keyframes lab-shift-dots { from { background-position: 0 0; } to { background-position: 24px 24px; } }
@keyframes lab-sweep { from { background-position: -12px 0; } to { background-position: 276px 0; } }
</style>
