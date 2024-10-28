<script setup lang="ts">

</script>
<template>
<div class="home-page">
  <RouterLink class="docs-icons" to="/doc">
    <div class="docs-text">
      <i class="iconfont icon-bianjiwenjian" />
      <span>文档</span>
    </div>
  </RouterLink>
</div>
</template>
<style scoped lang="less">
.home-page {
  display: flex;
  justify-content: center;
  margin-top: 80px;
  .docs-icons {
    display: inline-block;
    padding: 2px 30px 16px;
    background-color: #fff;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 2px 2px 4px #ccc;
    &:hover {
      box-shadow: 0 2px 7px rgba(55, 84, 104, 0.35);
      background-color: lighten(rgb(60, 196, 81), 40%);
    }
    .docs-text {
      text-align: center;
      i {
        display: block;
        font-size: 60px;
      }
      span {
        display: block;
        margin-top: -12px;
      }
    }
  }
}
</style>
