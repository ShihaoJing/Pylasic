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
    hasResult: false,
    resultList: []
  },
  methods: {
    submit: function () {
      var query = {
        queryString: this.queryString
      }
      this.$http.get('/q', {params: query}).then(response => {
        console.log(response.body)
        if (response.body.length == 0) {
          this.hasResult = false;
          this.resultList = []
        }
        else 
        {
          this.hasResult = true;
          this.resultList = response.body
        }
        //this.resultList = fakeRes;
      }, response => {
        // error callback
      });
    }
  }
})