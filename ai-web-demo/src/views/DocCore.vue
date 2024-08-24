<script setup lang="ts">
import { watchPostEffect, onMounted, ref, nextTick, computed } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.core.css'
import "quill/dist/quill.snow.css";
import { EventUtil, getElementLeft } from '@/utils/utils'

const editorContainerRef: any = ref(null)
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
  { label: '润色-口语化', value: 'polish-口语化' },
  { label: '润色-更活泼', value: 'polish-更活泼' },
  { label: '润色-更正式', value: 'polish-更正式' },
  { label: '续写', value: 'continue_writing' },
  { label: '缩短篇幅', value: 'shorten_text' },
  { label: '扩充篇幅', value: 'expand_text' },
]);
const question = ref('')
const content = ref(`小文盲在班里是学习最差的，整天像这假期该怎么玩，作业没有一天写完过。新学期又开始了，他背着仿佛千斤重的书包，在回家的路上。
      
忽然，他看见一个卖茶叶蛋的小摊。他克服不了见什么食物都馋的毛病，用妈妈给他买本子的两块钱买了四个茶叶蛋，刚放到嘴里，又念一想：我何必不开个卖茶叶蛋的小摊呢？这样既能赚钱，又能吃到自己爱吃的茶叶蛋，这不是两全其美吗？说干就干，他向妈妈要了1000元说要交学费，然后自己开了个卖茶叶蛋的小摊。花200元买了个炉子，写了个招牌，靠平时观察别人做茶叶蛋的方法做了起来，然后把课本当柴烧，扔进了炉子里。那个体营业证怎么办呢？他花高价请路人写了个个体营业证，挂在自己营业后面的墙上，还贴了张自己的照片。`)


let quillInst: any = null
let currentSelection: any = null

onMounted(() => {
  quillInst = new Quill('#editor', {
    theme: 'snow',
    placeholder: '输入问题，或从下方选择场景提问。',
  })
  quillInst.setContents([
    {
      insert: content.value,
    }
  ])

  // 监听右键事件
  editorContainerRef.value.addEventListener('contextmenu', async (event: any) => {
    event.preventDefault();
    currentSelection = quillInst.getSelection();
    showMenu.value = true;
    await nextTick(); // 确保Vue已更新DOM
    const popupEl: any = popupRef.value
    if (popupEl) {
      const left = getElementLeft(editorContainerRef.value)
      popupEl.style.position = 'absolute';
      popupEl.style.left = `${left + 15}px`;
      popupEl.style.top = `${event.clientY + 16}px`;
      // 记录回答内容需要展示的位置
      aiAnswerHandler.value.left = left + 15
      aiAnswerHandler.value.top = event.clientY + 16
    }
    questionRef.value.focus()
    if (currentSelection && currentSelection.length > 0) {
        // 应用高亮样式
        quillInst.formatText(currentSelection.index, currentSelection.length, {
            'background-color': '#d0eac8' // 使用内联样式直接设置背景色
        }, 'user');
    }
  });
})

const handleClickOutside = (e: any) => {
  const _isClickChildren = EventUtil.isClickChildren({
    event: e,
    classNames: ['input-box', 'dropdown-box', 'ai-answer-box'],
  })
  if (_isClickChildren) {
    return
  }
  setTimeout(() => {
    showMenu.value = false;
    if (currentSelection) {
      quillInst.removeFormat(currentSelection.index, currentSelection.length, 'user');
    }
  }, 0)
}

const handleSearchAI = (params: any) => {
  // 使用fetch()请求远程的流式API的返回
  fetching.value = true;
  aiAnswerHandler.value.show = true
  
  fetch(`http://127.0.0.1:8000/ai_polish/conversationId`, {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify({
      ...params,
      // engine: 'llama2',
    }),
  })
    .then(response => response.body)
    .then(async (body: any) => {
      // console.log('rb', rb);
      aiAnswer.value = ''
      let reader = body.getReader()
      while (true) {
        let { value, done } = await reader.read()
        // console.log('@@@@value', )
        aiAnswer.value += new TextDecoder().decode(value)
        if (done) {
          console.log('read done')
          fetching.value = false;
          break
        }
      }
    })
}

const handleClickCast = (item: any) => {
  // console.log('点击了', item)
  const value = item.value
  const [type, sub_type] = value.split('-')
  const params: any = {
    text: content.value,
    type,
  }
  if (sub_type) {
    params.sub_type = sub_type
  }
  // console.log('@@@@@@params', params)
  handleSearchAI(params)
  // modalInfo.value.visible = false;
}

const handleSubmitCustom = () => {
  // todo
  // const text = problem.value
  // problem.value = ''
  // modalInfo.value.visible = false;
  // handleSubmit({
  //   text: `"${content.value}"。${text}`,
  // }, 'ai_stream')
}

const handleBlur = () => {
  setTimeout(() => {
    // todo
    // modalInfo.value.foucsInput = false
  }, 200)
}

const isShowBottomBar = computed(() => {
  return !!aiAnswer.value && !fetching.value
})

</script>
<template>
  <div class="doc-core-box">
    <div ref="editorContainerRef" id="editor" class="doc-core-content"></div>
    <div v-show="showMenu" ref="popupRef">
      <div class="input-box" v-click-outside="handleClickOutside">
        <span class="input-box-icon">
          <el-icon style="vertical-align:-2px;"><Promotion /></el-icon>
        </span>
        <input v-model="question" ref="questionRef" 
            @keydown.enter="handleSubmitCustom" 
            placeholder="输入问题，或从下方选择场景提问。"
           @blur="handleBlur" />
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
          <span class="close-ai-answer">
            <el-icon><Close /></el-icon>
          </span>
        </span>
      </div>
      <div class="ai-answer-content">
        {{ aiAnswer }}
      </div>
      <div class="ai-answer-bottombar" v-if="isShowBottomBar">
        <el-button size="small">
          <el-icon><Select /></el-icon>
          替换原文
        </el-button>
        <el-button size="small">
          <el-icon><BottomLeft /></el-icon>
          插入下方
        </el-button>
        <el-tooltip
          effect="dark"
          content="复制"
          placement="bottom"
        >
          <el-button size="small">
            <el-icon><CopyDocument /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip
          effect="dark"
          content="删除"
          placement="bottom"
        >
          <el-button size="small">
            <el-icon><Delete /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip
          effect="dark"
          content="重写"
          placement="bottom"
        >
          <el-button size="small">
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

  .doc-core-content {
    min-height: calc(100vh - 64px);
  }
  
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
@doc-width: 960px;
.doc-core-box {
  .ql-container {
    width: @doc-width;
    margin: 0 auto 24px;
    box-shadow: rgba(0, 0, 0, 0.06) 0px 0px 10px 0px, rgba(0, 0, 0, 0.04) 0px 0px 0px 1px;
    border: none;
    background: #fff;
    font-size: 14px;
  }

  .ql-toolbar.ql-snow {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background-color: #f9fafb;
  }
}
</style>
