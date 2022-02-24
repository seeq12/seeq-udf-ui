<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="search_visible?'background-color:#F6F6F6; opacity: 1; height:220px; min-width: 300px':
      'display: none !important'"
  >

    <v-card-title>
      {{class_functionality}}
    </v-card-title>

    <v-container>
    <v-row no-gutters style="height: 50px;">
      <v-combobox
          :items="package_list"
          label="Select a package or type a new package name"
          v-model="selected_package"
          :rules="[v => !!v || 'Package name required']"
          @change="update_package_object">
      </v-combobox>
    </v-row>

      <v-spacer style="height: 15px;"></v-spacer>

    <v-row no-gutters style="height: 50px;">
      <v-combobox
          :items="function_list"
          label="Select a function or type a new function name"
          v-model="selected_function"
          :rules="[v => !!v || 'Function name required']"
          @change="update_function"
        >
      </v-combobox>


    </v-row>
    </v-container>
    <v-spacer style="height: 15px;"></v-spacer>

  </v-card>

</template>

