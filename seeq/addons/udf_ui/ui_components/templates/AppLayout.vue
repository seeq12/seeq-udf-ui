<template>
  <v-app id="udf-addon-app" style="max-width: 1000px; max-height: 1200px">
    <v-app-bar color="#007960" dark dense>
      <v-toolbar-title>User-Defined Formula Functions (UDFs) Editor</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-divider vertical></v-divider>
    </v-app-bar>

    <v-main>

      <div class="d-flex flex-column flex-wrap pr-3 pt-5" style="background-color: #F6F6F6; opacity: 1">
        <v-row no-gutters>
          <v-col cols="6">
            <search-display></search-display>
            <function-parameters-display></function-parameters-display>
          </v-col>

          <v-col cols="6">
            <function-documentation></function-documentation>
            <access-management></access-management>
            <summary-page></summary-page>
          </v-col>

          <v-snackbar :timeout="snackbar_timeout" :value="confirmation_snackbar_visible" :color="message_color"
                      absolute rounded="pill" top right text
          >
              <span v-html="success_failure_message"/>
              <v-spacer/>
              <v-btn icon @click="confirmation_snackbar_visible = false" top right>
                  <v-icon x-small>mdi-close</v-icon>
              </v-btn>
          </v-snackbar>

        </v-row>
      </div>
    </v-main>
  </v-app>
</template>

<style>
  #notebook { padding-top:0px !important; }
  .end_space { min-height:0px !important; }
  div.output_subarea.jupyter-widgets-view { max-width: 100%}
  #appmode-leave {display: none; !important;}
  #header #header-container {display: none !important;}

  .vuetify-styles .theme--light.primary{
    background-color: #007960 !important;
    color: whitesmoke !important;
  }

  .v-application .primary--text{
    color: #007960 !important;
    caret-color: #007960 !important;
  }

  .v-icon.notranslate.mdi.mdi-check.theme--light{
    font-size:1.2em; !important
  }
  .flex-column {
    display: flex;
    flex-flow: column wrap;
    justify-content: space-around;
  }

  .vuetify-styles .theme--light.v-list-item .v-list-item__action-text,
  .vuetify-styles .theme--light.v-list-item .v-list-item__subtitle {
    color: #212529;
  }

  .vuetify-styles .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) {
    color: #007960 !important;
  }

  .vuetify-styles .v-label {
    font-size: 14px;
  }

  .vuetify-styles .v-application {
    font-family: "Source Sans Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
  }

  .v-input{
      font-family: Courier;
  }
  .v-label{
      font-family: Helvetica;
      font-size:11px;
  }

  .v-list-item{
      font-family: Courier;
  }
</style>
<script>
module.exports = {
  created(){
    this.disable_scroll();
  },
  methods: {
    disable_scroll() {
      IPython.OutputArea.prototype._should_scroll = function (lines) {
        return false;
      }
    }
  }
}
</script>