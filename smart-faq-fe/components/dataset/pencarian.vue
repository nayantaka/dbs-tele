<template>
  <b-card class="mb-3" header="Pencarian">
    <b-form-row>
      <b-col md="6">
        <b-form-group
          label="Context"
          label-for="context"
          label-class="small"
        >
          <b-input
            id="context"
            placeholder="Context"
            @input="searchContext"
          />
        </b-form-group>
      </b-col>
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
    </b-form-row>
    <b-form-group
      label="Paragraph"
      label-for="paragraph"
      label-class="small"
      class="mb-0"
    >
      <b-input
        id="paragraph"
        placeholder="Paragraph"
        @input="searchParagraph"
      />
    </b-form-group>
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
    ...mapGetters('dataset', {
      categorys: 'category'
    }),
    cari () {
      const re = {}
      re.context = _.has(this.value, 'context') && !_.isEmpty(this.value.context) ? this.value.context : ''
      return re
    },
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
    searchContext (val) {
      const $value = { ...this.value }
      if (!_.isEmpty(val)) {
        $value.context = val
      } else {
        delete $value.context
      }
      this.$emit('input', $value)
    },
    searchIntent (val) {
      const $value = { ...this.value }
      if (!_.isEmpty(val)) {
        $value.intent = val
      } else {
        delete $value.intent
      }
      this.$emit('input', $value)
    },
    searchParagraph (val) {
      const $value = { ...this.value }
      if (!_.isEmpty(val)) {
        $value.paragraph = val
      } else {
        delete $value.paragraph
      }
      this.$emit('input', $value)
    }
  }
}
</script>
