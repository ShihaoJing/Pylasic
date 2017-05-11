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
    resultList: []
  },
  methods: {
    submit: function () {
      this.hasResult = true;
      showloader();
      var query = {
        queryString: this.queryString
      }
      this.$http.get('/q', {params: query}).then(response => {
        hideLoader();
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