<template>
  <b-card class="mb-3" header="Pencarian">
    <b-form-row>
      <b-col md="6">
        <b-form-group
          label="Intent"
          label-for="intent"
          label-class="small"
        >
          <b-select
            id="intent"
            :value="category"
            :options="categoryOpts"
            placeholder="Context"
            @input="searchIntent"
          />
        </b-form-group>
      </b-col>
      <b-col md="6">
        <b-form-group
          label="Response"
          label-for="response"
          label-class="small"
          class="mb-0"
        >
          <b-input
            id="response"
            placeholder="Response"
            @input="searchResponse"
          />
        </b-form-group>
      </b-col>
    </b-form-row>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    value: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  computed: {
    ...mapGetters('response', {
      categorys: 'category'
    }),
    category () {
      return _.has(this.value, 'category') && !_.isEmpty(this.value.category) ? {
        value: this.value.category,
        text: this.$tools.categoryNormalize(this.value.category)
      } : ''
    },
    categoryOpts () {
      const re = [
        {
          value: '', text: 'Silahkan Pilih'
        }
      ]
      if (_.isEmpty(this.categorys)) { return re }
      this.categorys.forEach((c) => {
        re.push({
          value: c,
          text: this.$tools.categoryNormalize(c)
        })
      })
      return re
    }
  },
  methods: {
    searchIntent (val) {
      const $value = { ...this.value }
      if (!_.isEmpty(val)) {
        $value.intent = val
      } else {
        delete $value.intent
      }
      this.$emit('input', $value)
    },
    searchResponse (val) {
      const $value = { ...this.value }
      if (!_.isEmpty(val)) {
        $value.response = val
      } else {
        delete $value.response
      }
      this.$emit('input', $value)
    }
  }
}
</script>
