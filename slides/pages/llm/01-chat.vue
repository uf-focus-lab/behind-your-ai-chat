<script setup lang="ts">
// The hello-world exchange in a chat window. The user's words are already
// split into the model's tokens, each carrying a view-transition-name, so the
// next slide can pull them out of the bubble into a token stream. The reply
// appears once demo/lib/figures/llm.py has run with an API key in .env; until
// then the assistant is typing.
import ChatWindow from '../../components/ChatWindow.vue'
import { useChatSend } from '../../composables/chatSend'
import data from '../../assets/llm/stream.json'

const user = data.stream.find((m) => m.role === 'user')!.tokens
const agent = data.stream.find((m) => m.role === 'assistant')?.tokens
const phase = useChatSend()
</script>

<template>
  <ChatWindow :phase="agent ? phase : Math.min(phase, 2)" height="396px" typing-vt="tok-a-typing">
    <template #user><span v-for="(t, i) in user" :key="i" :style="{ viewTransitionName: `tok-u-${i}` }">{{ t.token }}</span></template>
    <template #agent><span v-for="(t, i) in agent" :key="i" :style="{ viewTransitionName: `tok-a-${i}` }">{{ t.token }}</span></template>
  </ChatWindow>
</template>
