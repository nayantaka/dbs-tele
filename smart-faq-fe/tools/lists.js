export default [
  {
    name: 'Core',
    menus: [
      {
        name: 'Dashboard',
        icon: ['fas', 'tachometer-alt'],
        to: '/'
      }
    ]
  },
  {
    name: 'Data',
    menus: [
      {
        name: 'Dataset',
        icon: ['fas', 'archive'],
        to: '/dataset'
      },
      {
        name: 'Response',
        icon: ['fas', 'reply'],
        to: '/response'
      },
      {
        name: 'Api Key',
        icon: ['fas', 'key'],
        to: '/api-key'
      }
    ]
  }
]
