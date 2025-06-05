<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  initialItems: { type: Array, required: false },
});

const batchSize = 30;
const windowSize = 90; // Keep 3 batches in memory
const visible = ref([]);
const loadedCount = ref(0);

function hydrate() {
  if (Array.isArray(props.initialItems) && props.initialItems.length) {
    visible.value = props.initialItems.slice(0, batchSize);
    loadedCount.value = batchSize;
  } else {
    visible.value = [];
    loadedCount.value = 0;
  }
}

hydrate();
watch(() => props.initialItems, hydrate);

function showNext() {
  if (!Array.isArray(props.initialItems)) return;

  const next = props.initialItems.slice(
    loadedCount.value,
    loadedCount.value + batchSize
  );
  
  if (next.length) {
    // Add new items
    visible.value.push(...next);
    loadedCount.value += next.length;
    
    // Remove old items if we exceed window size
    if (visible.value.length > windowSize) {
      const removeCount = visible.value.length - windowSize;
      visible.value = visible.value.slice(removeCount);
    }
  }
}

function observe(lastEl) {
  if (!lastEl) return;
  const io = new IntersectionObserver(([e]) => {
    if (e.isIntersecting) {
      io.disconnect();
      showNext();
    }
  }, { 
    threshold: 0.5,
    rootMargin: '100px' // Start loading before reaching the bottom
  });
  io.observe(lastEl);
}

onMounted(() => {
  watch(
    visible,
    () => observe(document.querySelector('#gallery li:last-child')),
    { flush: 'post' }
  );
});

</script>

<template>
  <!-- 1-col mobile, 3-col desktop, 1-px gaps -->
  <ul id="gallery" class="grid gap-px grid-cols-1 md:grid-cols-3">
    <li v-for="(item, i) in visible" :key="i">
      <component
        :is="item.type === 'video' ? 'video' : 'img'"
        :src="item.src"
        :alt="item.alt"
        class="w-full h-auto"
        v-bind="item.type === 'video'
          ? { muted: true, autoplay: true, loop: true, playsinline: true }
          : { loading: 'lazy' }"
      />
    </li>
  </ul>
</template>