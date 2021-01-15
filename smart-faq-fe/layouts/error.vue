<template>
  <b-col lg="6">
    <div class="text-center mt-4">
      <h1 class="display-1">
        {{ error.statusCode }}
      </h1>
      <p>
        {{ error.message }}
      </p>
      <b-link to="/">
        <fa-layers class="fa-fw">
          <fa-icon :icon="['fas', 'arrow-left']" />
        </fa-layers>
        Kembali Halaman Awal
      </b-link>
    </div>
  </b-col>
</template>

<script>
export default {
  // eslint-disable-next-line vue/require-prop-types
  props: ['error'],
  layout: 'error-layout'
}
</script>
