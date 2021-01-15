<template>
  <b-row>
    <b-col cols="12">
      <h1 class="mt-4">
        {{ title }}
      </h1>
      <b-breadcrumb :items="breadcrumb" class="mb-4" />
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters('page-title', {
      title: 'title',
      breadcrumb: 'breadcrumb'
    })
  }
}
</script>
