<script setup lang="ts">
// VL-Explore running: the lecturer's own robot, steered by CLIP alone. The
// brief fills the slide and is played by hand from the controls bar; leaving
// the slide pauses it so it does not keep talking from the next slide.
import { onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive } from '@slidev/client'
import clip from '../../assets/vlfm/vlx-brief.webm'

const active = useIsSlideActive()
const video = ref<HTMLVideoElement>()
watch(active, (on) => {
  if (!on) video.value?.pause()
})
onBeforeUnmount(() => video.value?.pause())
</script>

<template>
  <video
    ref="video"
    :src="clip"
    class="vlfm-vlx-video"
    controls
    playsinline
    preload="metadata"
  />
</template>

<style scoped>
.vlfm-vlx-video {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000;
}
</style>
