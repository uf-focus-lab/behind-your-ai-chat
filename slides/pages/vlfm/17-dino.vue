<script setup lang="ts">
// Why a second encoder: the same photograph, CLIP's patch vectors and
// DINOv2's, each painted by PCA. CLIP's are blurry because only its class
// token was ever trained; DINOv2 trains the patches themselves. Under it,
// the two lines of successors. Pictures from demo/lib/figures/clip.py and
// demo/lib/figures/dino.py.
import Stage from '../../components/Stage.vue'
import photo from '../../assets/vlfm/dog_a-square.webp'
import clipPatches from '../../assets/vlfm/clip-patches.webp'
import dinoPatches from '../../assets/vlfm/dino-patches.webp'
import clipMeta from '../../assets/vlfm/clip-outputs.json'
import dinoMeta from '../../assets/vlfm/dino-outputs.json'

const panels = [
  { src: photo, label: 'the photograph', sub: '' },
  { src: clipPatches, label: 'CLIP ViT-B/32', sub: `${clipMeta.grid} × ${clipMeta.grid} patches, trained only through the class token` },
  { src: dinoPatches, label: 'DINOv2 ViT-S/14', sub: `${dinoMeta.grid} × ${dinoMeta.grid} patches, trained patch by patch, no labels` },
]
</script>

<template>
  <Stage gap="0.9rem">
    <div class="vlfm-dino-row">
      <figure v-for="p in panels" :key="p.label" class="vlfm-dino-panel">
        <img :src="p.src" :alt="p.label" />
        <figcaption><b>{{ p.label }}</b><span v-if="p.sub">{{ p.sub }}</span></figcaption>
      </figure>
    </div>
    <div class="vlfm-dino-lines">
      <div class="vlfm-dino-line">
        <span class="vlfm-dino-head">knows words</span>
        <span class="vlfm-dino-step">CLIP <span class="vlfm-dino-year">2021</span></span>
        <span class="vlfm-dino-arrow">→</span>
        <span class="vlfm-dino-step">SigLIP <span class="vlfm-dino-year">2023</span></span>
      </div>
      <div class="vlfm-dino-line">
        <span class="vlfm-dino-head">knows where</span>
        <span class="vlfm-dino-step">DINO <span class="vlfm-dino-year">2021</span></span>
        <span class="vlfm-dino-arrow">→</span>
        <span class="vlfm-dino-step">DINOv2 <span class="vlfm-dino-year">2024</span></span>
        <span class="vlfm-dino-arrow">→</span>
        <span class="vlfm-dino-step">DINOv3 <span class="vlfm-dino-year">2025</span></span>
      </div>
    </div>
  </Stage>
</template>

<style scoped>
.vlfm-dino-row { display: flex; gap: 1.2rem; align-items: flex-start; }
.vlfm-dino-panel { margin: 0; width: 250px; display: flex; flex-direction: column; gap: 0.4rem; }
.vlfm-dino-panel img { width: 250px; height: 250px; border-radius: 8px; object-fit: cover; }
.vlfm-dino-panel figcaption { display: flex; flex-direction: column; font-size: 16px; line-height: 1.3; color: var(--ink-faint); }
.vlfm-dino-panel figcaption b { font-weight: 600; color: var(--ink-strong); }
.vlfm-dino-lines { display: flex; flex-direction: column; align-items: center; gap: 0.35rem; font-size: 19px; color: var(--ink); }
.vlfm-dino-line { display: flex; align-items: baseline; gap: 0.5rem; }
.vlfm-dino-head { font-variant: small-caps; letter-spacing: 0.02em; color: var(--accent); margin-right: 0.3rem; white-space: nowrap; }
.vlfm-dino-step { color: var(--ink-strong); white-space: nowrap; }
.vlfm-dino-year { font-size: 15px; color: var(--ink-faint); }
.vlfm-dino-arrow { color: var(--ink-soft); }
</style>
