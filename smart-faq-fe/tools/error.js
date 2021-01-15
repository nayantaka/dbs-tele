const initOpts = {
  code: 'E_ERROR',
  name: 'Error',
  message: 'Error with unknown'
}

export default function (opts = {}, err = new Error()) {
  let reOpts
  if (_.isEmpty(err) || !_.isError(err)) {
    err = new Error()
  }
  if (_.isString(opts)) {
    reOpts = {
      ...initOpts,
      message: opts
    }
  } else if (_.isObject(opts) && !_.isArray(opts)) {
    if (_.has(opts, 'response')) {
      const { response: { data, status } } = opts
      if (_.isString(data)) {
        reOpts = {
          ...initOpts,
          message: data
        }
      } else if (_.isObject(data) && !_.isArray(data)) {
        reOpts = {
          code: _.has(data, 'code') && !_.isEmpty(data.code) ? data.code : initOpts.code,
          name: _.has(data, 'name') && !_.isEmpty(data.name) ? data.name : initOpts.name,
          message: (function () {
            if (_.has(data, 'msg') && !_.isEmpty(data.msg)) {
              return data.msg
            }
            if (_.has(data, 'message') && !_.isEmpty(data.message)) {
              return data.message
            }
            return initOpts.message
          })()
        }
      } else {
        reOpts = {
          ...initOpts,
          status,
          message: `Error with status ${status}`
        }
      }
    } else if (_.has(opts, 'request')) {
      const { request: { status } } = opts
      reOpts = {
        ...initOpts,
        status,
        message: `Error with status ${status}`
      }
    } else {
      reOpts = {
        code: _.has(opts, 'code') && !_.isEmpty(opts.code) ? opts.code : initOpts.code,
        name: _.has(opts, 'name') && !_.isEmpty(opts.name) ? opts.name : initOpts.name,
        message: (function () {
          if (_.has(opts, 'msg') && !_.isEmpty(opts.msg)) {
            return opts.msg
          }
          if (_.has(opts, 'message') && !_.isEmpty(opts.message)) {
            return opts.message
          }
          return initOpts.message
        })()
      }
    }
  } else {
    reOpts = { ...initOpts }
  }
  _.extend(err, reOpts)
  return err
}
