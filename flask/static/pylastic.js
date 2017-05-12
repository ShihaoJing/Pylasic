function hideLoader() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("content").style.display = "block";
}

function showloader() {
  document.getElementById("content").style.display = "none";
  document.getElementById("loader").style.display = "block";
}

new Vue({
  el: '#app',
  data: {
    queryString: '',
    hasResult: false,
    hasError: false,
    resultList: [],
    errorMessage: ''
  },
  methods: {
    submit: function () {
      showloader();
      var query = {
        queryString: this.queryString
      }
      this.$http.get('/q', {params: query}).then(response => {
        hideLoader();
        console.log(response.body)
        if (response.body.length == 0) {
          this.hasResult = false;
          this.hasError = false;
          this.resultList = []
        }
        else 
        {
          this.resultList = response.body
          if ('Error' in this.resultList[0]) {
            this.errorMessage = this.resultList[0]['Error']
            this.hasError = true;
            this.hasResult = true;
          }
          else
          {
            this.hasResult = true;
            this.hasError = false;
          }
        }
        //this.resultList = fakeRes;
      }, response => {
        // error callback
      });
    }
  }
})