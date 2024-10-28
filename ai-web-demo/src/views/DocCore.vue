<script setup lang="ts">
import { watchPostEffect, onMounted, ref, nextTick, computed, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useClipboard } from '@vueuse/core'

import { fetchAI } from '@/services/'
import { EventUtil, getElementLeft } from '@/utils/utils'
import QuillEditor from '@/components/QuillEditor/index.vue'

import "quill/dist/quill.snow.css";

const { copy } = useClipboard({ source: '' })

// const editorContainerRef: any = ref(null)
const quillEditorRef = ref(null)

const popupRef: any = ref(null)
const dropdownRef: any = ref(null)
const questionRef: any = ref(null)
const showMenu = ref(false)
const fetching = ref(false)
const aiAnswer = ref('')
const aiAnswerHandler = ref({
  show: false,
  left: 0,
  top: 0,
})
const castList = ref([
  { label: '润色-口语化', value: 'polish-colloquial' },
  { label: '润色-更活泼', value: 'polish-lively' },
  { label: '润色-更正式', value: 'polish-formal' },
  { label: '续写', value: 'continue_writing' },
  { label: '缩短篇幅', value: 'shorten' },
  { label: '扩充篇幅', value: 'expand' },
]);
const question = ref('')
const content = ref(`小文盲在班里是学习最差的，整天像这假期该怎么玩，作业没有一天写完过。新学期又开始了，他背着仿佛千斤重的书包，在回家的路上。
      
忽然，他看见一个卖茶叶蛋的小摊。他克服不了见什么食物都馋的毛病，用妈妈给他买本子的两块钱买了四个茶叶蛋，刚放到嘴里，又念一想：我何必不开个卖茶叶蛋的小摊呢？这样既能赚钱，又能吃到自己爱吃的茶叶蛋，这不是两全其美吗？说干就干，他向妈妈要了1000元说要交学费，然后自己开了个卖茶叶蛋的小摊。花200元买了个炉子，写了个招牌，靠平时观察别人做茶叶蛋的方法做了起来，然后把课本当柴烧，扔进了炉子里。那个体营业证怎么办呢？他花高价请路人写了个个体营业证，挂在自己营业后面的墙上，还贴了张自己的照片。`)

// 记录上一次请求AI接口的参数，重新生成的时候使用
let preAIParams: any = null

let lastCommandPressTime: number | null = null;
const commandKey = 'Meta'; // 对应 Mac 的 Command 键
const ctrlKey = 'Control'; // 对应 Windows 的 Ctrl 键

const handleDblclick = async (event: any) => {
    showMenu.value = true;
    await nextTick(); // 确保Vue已更新DOM
    const popupEl: any = popupRef.value
    if (popupEl) {
      const editorEl = document.getElementById('doc-core-id')
      if (!editorEl) {
        ElMessage.error({
          message: '获取编辑器失败!',
          type: 'error',
          duration: 0,
        })
        return
      }
      const left = getElementLeft(editorEl)
      popupEl.style.position = 'absolute';
      popupEl.style.left = `${left + 15}px`;
      popupEl.style.top = `${event.clientY + 16}px`;
      // 记录回答内容需要展示的位置
      aiAnswerHandler.value.left = left + 15
      aiAnswerHandler.value.top = event.clientY + 16
    }
    questionRef.value.focus()
}

const closeAiAnserPopup = () => {
  aiAnswerHandler.value.show = false
  aiAnswer.value = ''
  quillEditorRef.value && (quillEditorRef.value as any).clearFormat()
}

let confirmThrowAwayCount = 0
const confirmThrowAway = () => {
  // 可能多次触发,使用一个计数器控制
  if (confirmThrowAwayCount > 0) {
    return
  }
  confirmThrowAwayCount += 1
  ElMessageBox.confirm(
    '确定要丢弃当前内容吗?',
    '丢弃提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
      confirmThrowAwayCount -= 1
      closeAiAnserPopup()
    })
    .catch(() => {
      confirmThrowAwayCount -= 1
    })
}

// 可能多次触发
const handleClickOutside = (e: any) => {
  // debugger
  const _isClickChildren = EventUtil.isClickChildren({
    event: e,
    classNames: ['input-box', 'dropdown-box', 'ai-answer-box'],
  })
  if (_isClickChildren) {
    return
  }
  showMenu.value = false;
  if (aiAnswerHandler.value.show) {
    confirmThrowAway()
    return
  }
  quillEditorRef.value && (quillEditorRef.value as any).clearFormat()
}

const handleSearchAI = async (params: any) => {
  // 使用fetch()请求远程的流式API的返回
  fetching.value = true;
  aiAnswerHandler.value.show = true
  if (params.question === undefined) {
    params.question = ''
  }
  preAIParams = params
  const streamReader = await fetchAI(params)
  if (streamReader) {
    while (true) {
      let { value, done } = await streamReader.read()
      aiAnswer.value += new TextDecoder().decode(value)
      if (done) {
        fetching.value = false;
        break
      }
    }
  }
}

const handleClickCast = (item: any) => {
  const value = item.value
  const [op_type, op_sub_type] = value.split('-')
  const content = (quillEditorRef.value as any).getText()
  const params: any = {
    content,
    op_type,
  }
  if (op_sub_type) {
    params.op_sub_type = op_sub_type
  }
  handleSearchAI(params)
  showMenu.value = false;
}

const handleSubmitCustom = () => {
  const content = (quillEditorRef.value as any).getText()
  handleSearchAI({
    content,
    question: question.value,
  })
  question.value = ''
  showMenu.value = false;
}

const handleReplace = () => {
  if (!aiAnswer.value) {
    ElMessage.warning('没有AI生成的内容')
    return
  }
  (quillEditorRef.value as any).replace(aiAnswer.value)
  closeAiAnserPopup()
}

const handleInsert = () => {
  if (!aiAnswer.value) {
    ElMessage.warning('没有AI生成的内容')
    return
  }
  (quillEditorRef.value as any).insert(aiAnswer.value)
  closeAiAnserPopup()
}

const handleCopy = () => {
  if (!aiAnswer.value) {
    ElMessage.warning('没有AI生成的内容')
    return
  }
  copy(aiAnswer.value)
  closeAiAnserPopup()
  ElMessage.success('复制成功')
}

const handleRegenerate = async (event: Event) => {
  if (!aiAnswer.value) {
    ElMessage.warning('没有AI生成的内容')
    return
  }
  event.preventDefault()
  event.stopPropagation()
  aiAnswer.value = ''
  // 重新生成
  handleSearchAI(preAIParams)
}

const isShowBottomBar = computed(() => {
  return !!aiAnswer.value && !fetching.value
})

const handleKeyDown = (event: KeyboardEvent) => {
      const currentTime = new Date().getTime();
      const key = event.key;

      if (key === commandKey || key === ctrlKey) {
        if (lastCommandPressTime && (currentTime - lastCommandPressTime) < 500) {
          // 如果两次按键间隔小于500毫秒，认为是连续按键
          const quillInstance = (quillEditorRef.value as any).getQuillInst()
          const editorElement = (quillEditorRef.value as any).getEditor()
          if (quillInstance) {
            const range = quillInstance.getSelection();
            if (range) {
              const bounds = quillInstance.getBounds(range.index);
              // const editorElement = editor.value;
              if (editorElement) {
                const rect = editorElement.getBoundingClientRect();
                handleDblclick({
                  clientY: rect.top + bounds.top,
                })
              }
            }
          }
        }
        lastCommandPressTime = currentTime;
      }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

</script>
<template>
  <div class="doc-core-box">
     <QuillEditor 
      ref="quillEditorRef"
      :content="content"
      :class-list="['doc-core-content']"
      id="doc-core-id"
      @on-dblclick="handleDblclick"
     />
    <div v-show="showMenu" ref="popupRef">
      <div class="input-box" v-click-outside="handleClickOutside">
        <span class="input-box-icon">
          <el-icon style="vertical-align:-2px;"><Promotion /></el-icon>
        </span>
        <input v-model="question" ref="questionRef" 
            @keydown.enter="handleSubmitCustom" 
            placeholder="输入问题，或从下方选择场景提问。" />
        <span class="send-btn" :class="[question ? 'active' : '']" @click="handleSubmitCustom">发送</span>
      </div>
      <div ref="dropdownRef" class="dropdown-box" v-click-outside="handleClickOutside">
          <ul>
            <li v-for="item in castList" :key="item.value" @click="handleClickCast(item)">
              {{ item.label }}
            </li>
          </ul>
        </div>
    </div>
    <!-- 回答的内容 -->
     <div 
      class="ai-answer-box" 
      :style="{ left: `${aiAnswerHandler.left}px`, top: `${aiAnswerHandler.top}px` }"
      v-if="aiAnswerHandler.show">
      <div class="ai-answer-topbar">
        <span>
          AI生成结果
          <el-icon class="loader" v-if="fetching"><Loading /></el-icon>
        </span>
        <span>
          <span class="close-ai-answer" @click="confirmThrowAway">
            <el-icon><Close /></el-icon>
          </span>
        </span>
      </div>
      <div class="ai-answer-content">
        {{ aiAnswer }}
      </div>
      <div class="ai-answer-bottombar" v-if="isShowBottomBar">
        <el-button size="small" @click="handleReplace">
          <el-icon><Select /></el-icon>
          替换原文
        </el-button>
        <el-button size="small" @click="handleInsert">
          <el-icon><BottomLeft /></el-icon>
          插入下方
        </el-button>
        <el-tooltip
          effect="dark"
          content="复制"
          placement="bottom"
        >
          <el-button size="small" @click="handleCopy">
            <el-icon><CopyDocument /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip
          effect="dark"
          content="重新生成"
          placement="bottom"
        >
          <el-button size="small" @click="handleRegenerate">
            <el-icon><RefreshLeft /></el-icon>
          </el-button>
        </el-tooltip>
      </div>
     </div>
  </div>
</template>
<style scoped lang="less">
.doc-core-box {
  position: relative;
  background: #f9fafb;
  padding-top: 44px;

  // .doc-core-content {
  //   min-height: calc(100vh - 64px);
  // }
  
  .ai-answer-box {
    position: absolute;
    border: 2px solid rebeccapurple;
    background-color: #fff;
    border-radius: 8px;
    min-height: 100px;
    padding: 8px 12px;
    width: 680px;
    .ai-answer-topbar {
      display: flex;
      justify-content: space-between;
      color: #999;
      font-size: 14px;
      .close-ai-answer {
        cursor: pointer;
        &:hover {
          color: #767676;
        }
      }
    }
    .ai-answer-content {
      margin-top: 6px;
      text-align: justify;
      max-height: 200px;
      overflow: auto;
      font-size: 14px;
      line-height: 22px;
    }
    .ai-answer-bottombar {
      margin-top: 8px;
    }
  }

  .input-box {
    display: flex;
    width: 100%;
    height: 48px;
    // padding-left: 40px;
    background-color: #000;
    border-radius: 8px;

    .input-box-icon {
      color: #fff;
      padding: 0 12px;
      line-height: 46px;
    }

    .send-btn {
      color: #767676;
      padding: 0 12px;
      line-height: 46px;
      cursor: pointer;

      &.active {
        color: #fff;
      }
    }

    input {
      flex: 1 auto;
      width: 500px;
      background-color: #000;
      border: none;
      outline: none;
      color: #fff;
      font-size: 16px;
    }
  }

  .dropdown-box {
    display: inline-block;
    // border: 1px solid #e4e7ed;
    border-radius: 4px;
    padding: 12px 6px;
    background-color: lighten(#000, 20%);
    border-radius: 4px;
    color: #fff;

    ul {
      list-style: none;
      padding: 0;

      li {
        padding: 0 12px;
        line-height: 32px;
        border-radius: 4px;
        cursor: pointer;

        &:hover {
          background-color: #767676;
        }
      }
    }
  }
  .loader {
    animation: spin 2s linear infinite;
  }
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
<style lang="less">
.doc-core-box {
  .doc-core-content {
    min-height: calc(100vh - 64px);
  }
}
</style>
