$(document).ready(function () {
    console.log("layerJS", layerJS);
  
    var app = new Vue({
      delimiters: ["[[", "]]"],
      el: "#app",
      data: {
        message: "Hello Vue!",
        checked: true,
        currentframe: "?"
      },
      computed: {
        mode: function () {
          return this.checked ? "editing zones" : "presenting";
        }
      },
  
      methods: {
        calc_curr_frame: function () {
          this.currentframe =
            layerJS.select("#mainlayer") == undefined
              ? "?"
              : layerJS.select("#mainlayer").currentFrame.name();
        },
        spawn_frame: function () {
          let b = {
            width: 150,
            height: 60,
          };
          let $dynamic_div = $(document.createElement("div")).css(b);
          $dynamic_div.attr('data-lj-type', 'frame')
          $dynamic_div.attr("data-lj-type", "frame");
          $dynamic_div.attr("data-lj-fit-to", "contain");
          $dynamic_div.attr("data-lj-name", "4");
          $dynamic_div.attr("data-lj-x", "300");
          $dynamic_div.attr("data-lj-y", "10");
          $dynamic_div.attr("data-lj-neighbors.b", "overview");
          $dynamic_div.attr("data-lj-neighbors.t", "3");
          $dynamic_div.appendTo("#mainlayer > div:nth-child(1)");
        }
      } // methods
    }); // vue
  
    $('[data-lj-type="frame"]').on("click", function (e) {
      // "1", "2", etc. or "overview"
      let zone = e.currentTarget._ljView.name();
      layerJS.select('[data-lj-type="layer"]').transitionTo(zone);
      app.calc_curr_frame();
    });
  
    // Shortcut keys
    $(document).keydown(function (e) {
      console.log(e.which);
  
      if ([37, 33, 38].includes(e.which))
        // 37 = LEFT, 33 = PGUP, 38 = UP arrow key
        layerJS
          .select('[data-lj-type="layer"]')
          .transitionTo(layerJS.select("#mainlayer").currentFrame.neighbors().t);
  
      if ([39, 34, 40].includes(e.which)) {
        // 39 = RIGHT, 34 = PGDOWN, 40 = DOWN arrow key
        let neighbors = layerJS.select("#mainlayer").currentFrame.neighbors();
        layerJS.select('[data-lj-type="layer"]').transitionTo(neighbors.b);
      }
  
      if (e.which == 27)
        // ESC
        layerJS.select('[data-lj-type="layer"]').transitionTo("overview");
    });
  
    app.calc_curr_frame();
  }); // doc ready
  