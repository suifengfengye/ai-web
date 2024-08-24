<template>
  <div ref="editorContainer" class="editor-container"></div>
  <el-dropdown v-if="showMenu" :show-timeout="0" :hide-timeout="0" @command="handleCommand">
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item v-for="item in castList" :key="item.value" :command="item.value">
          {{ item.label }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import 'element-plus/dist/index.css';
import { ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus';

const editorContainer = ref(null);
const showMenu = ref(false);
const castList = ref([
  { label: '润色-口语化', value: 'polish-口语化' },
  { label: '润色-更活泼', value: 'polish-更活泼' },
  { label: '润色-更正式', value: 'polish-更正式' },
  { label: '续写', value: 'continue_writing' },
  { label: '缩短篇幅', value: 'shorten_text' },
  { label: '扩充篇幅', value: 'expand_text' },
]);

let quill;

onMounted(() => {
  quill = new Quill(editorContainer.value, {
    theme: 'snow'
  });

  editorContainer.value.addEventListener('contextmenu', (event) => {
    event.preventDefault();
    showMenu.value = true;
    // Position the menu
    document.querySelector('.el-dropdown').style.position = 'absolute';
    document.querySelector('.el-dropdown').style.left = `${event.clientX}px`;
    document.querySelector('.el-dropdown').style.top = `${event.clientY}px`;
  });

  document.addEventListener('click', () => {
    showMenu.value = false;
  });
});

function handleCommand(command) {
  console.log('Selected command:', command);
  showMenu.value = false;
}
</script>

<style>
.editor-container {
  height: 300px;
}
</style>
