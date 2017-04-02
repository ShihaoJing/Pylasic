var fakeRes = [
  {
      'title': '1st dataset',
      'text': "I'm the first data set"
  },
  {
      'title': '2nd dataset',
      'text': "I'm the second data set"
  },
  {
      'title': '3rd dataset',
      'text': "I'm the third data set"
  }
]

new Vue({
  el: '#app',
  data: {
    queryString: '',
    resultList: []
  },
  methods: {
    submit: function () {
      this.$http.get('/q').then(response => {
        console.log(response.body)
        //this.resultList = response.body
        this.resultList = fakeRes;
      }, response => {
        // error callback
      });
    }
  }
})