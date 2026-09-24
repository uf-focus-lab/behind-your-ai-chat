<script setup lang="ts">
// The chat window again, with a photograph in the user's bubble. The picture
// is drawn as a 7 × 7 grid of tiles, seamless here, each with its own
// view-transition-name, so the next slide can pull the tiles apart into
// tokens the way it pulled the words apart. The question's and the reply's
// tokens carry names too. Reply and tile count from demo/lib/figures/vision.py.
import ChatWindow from '../../components/ChatWindow.vue'
import { useChatSend } from '../../composables/chatSend'
import data from '../../assets/vlfm/stream-vision.json'
import photo from '../../assets/vlfm/dog_a-square.webp'

const GRID = 7
const TILE = 22
const phase = useChatSend()
const tiles = Array.from({ length: GRID * GRID }, (_, i) => ({
  vt: `img-${i}`,
  style: {
    backgroundImage: `url(${photo})`,
    backgroundSize: `${GRID * TILE}px ${GRID * TILE}px`,
    backgroundPosition: `${-(i % GRID) * TILE}px ${-Math.floor(i / GRID) * TILE}px`,
  },
}))
</script>

<template>
  <ChatWindow :phase="phase" height="500px" style="--chat-bubble-w: 540px">
    <template #user>
      <div class="vlfm-chat-photo">
        <div class="vlfm-chat-grid"><span v-for="t in tiles" :key="t.vt" class="vlfm-chat-tile" :style="{ ...t.style, viewTransitionName: t.vt }" /></div>
        <p class="vlfm-chat-text"><span v-for="(t, i) in data.question" :key="i" :style="{ viewTransitionName: `tok-q-${i}` }">{{ t.token }}</span></p>
      </div>
    </template>
    <template #agent><span v-for="(t, i) in data.reply" :key="i" :style="{ viewTransitionName: `tok-r-${i}` }">{{ t.token }}</span></template>
  </ChatWindow>
</template>

<style scoped>
.vlfm-chat-photo { display: flex; flex-direction: column; gap: 0.5rem; }
/* clip-path rather than overflow: the scaled tiles are transformed, and a
   border-radius clip does not hold on all four corners for them */
.vlfm-chat-grid { display: grid; grid-template-columns: repeat(7, 22px); clip-path: inset(0 round 10px); }
/* a hair of overlap hides the seams the slide scaling leaves between tiles */
.vlfm-chat-tile { display: block; width: 22px; height: 22px; background-repeat: no-repeat; transform: scale(1.04); }
p.vlfm-chat-text { margin: 0; }
</style>
