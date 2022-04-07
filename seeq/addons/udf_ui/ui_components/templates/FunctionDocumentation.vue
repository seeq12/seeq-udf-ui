<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="description_visible?'background-color:#F6F6F6; opacity: 1; min-width: 300px': 'display: none !important'"
  >
    <v-card-title>
      {{class_functionality}}
    </v-card-title>

    <v-subheader style="height: fit-content; padding-bottom: 15px; font-size: 12px">
      Enter markdown or html to update package or function description. Use the Examples button to edit examples.
    </v-subheader>

    <v-container fluid v-show="description_visible && package_description_toggle==0" style="margin: 0px">
      <v-textarea
        name="package description markdown"
        clear-icon="mdi-close-circle"
        label="Package Markdown"
        outlined
        :value="package_description_markdown"
        v-model="package_description_markdown"
        multiple
        @input="update_package_desc_html"
        no-resize="true"
        wrap="off"
        height="100"
        hide-details
      ></v-textarea>
    </v-container>
    <v-container fluid v-show="description_visible && package_description_toggle==1" style="margin: 0px">
      <v-textarea
        name="description html raw"
        clear-icon="mdi-close-circle"
        label="Package Raw HTML"
        outlined
        :value="package_description_html"
        v-model="package_description_html"
        @input="update_package_desc_markdown"
        no-resize="true"
        wrap="off"
        height="100"
        hide-details
      ></v-textarea>
      </v-container>
    <v-container fluid v-show="description_visible && package_description_toggle==2">
        <v-header style="font-size: 10.5px; font-family: Helvetica; color: #616161; margin: 6px;">
          Package Processed HTML
        </v-header>
         <v-card class="pa-2" elevation="0" color="#F6F6F6" style="margin: 0px; border: 1px solid #C6C6C6;">
           <div v-html="package_description_html" class="text-left"/>
         </v-card>
      </v-container>

        <v-container fluid style="margin: 0px; padding-top: 0px">
      <v-btn-toggle v-model="package_description_toggle" mandatory style="margin: 0px">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small v-bind="attrs" v-on="on">
              <v-icon small>mdi-pound</v-icon>
            </v-btn>
          </template>
          <span>Markdown</span>
      </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small v-bind="attrs" v-on="on">
              <v-icon small>mdi-xml</v-icon>
            </v-btn>
          </template>
          <span>html</span>
      </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small v-bind="attrs" v-on="on">
              <v-icon small>mdi-text-subject</v-icon>
            </v-btn>
          </template>
          <span>Final</span>
      </v-tooltip>
      </v-btn-toggle>
    </v-container>

    <v-subheader style="height: fit-content; padding-bottom: 15px; font-size: 12px">
      Function description:
    </v-subheader>

    <v-container fluid v-show="description_visible && func_description_toggle==0" style="margin: 0px">
      <v-textarea
        name="description markdown"
        clear-icon="mdi-close-circle"
        label="Function Markdown"
        outlined
        :value="func_description_markdown"
        v-model="func_description_markdown"
        multiple
        @input="update_func_desc_html"
        no-resize="true"
        wrap="off"
        height="200"
        hide-details
      ></v-textarea>
    </v-container>
    <v-container fluid v-show="description_visible && func_description_toggle==1" style="margin: 0px">
      <v-textarea
        name="description html raw"
        clear-icon="mdi-close-circle"
        label="Function Raw HTML"
        outlined
        :value="func_description_html"
        v-model="func_description_html"
        @input="update_func_desc_markdown"
        no-resize="true"
        wrap="off"
        height="200"
        hide-details
      ></v-textarea>
      </v-container>
    <v-container fluid v-show="description_visible && func_description_toggle==2">
        <v-header style="font-size: 10.5px; font-family: Helvetica; color: #616161; margin: 6px;">
          Function Processed HTML
        </v-header>
         <v-card class="pa-2" elevation="0" color="#F6F6F6" style="margin: 0px; border: 1px solid #C6C6C6;">
           <div v-html="func_description_html" class="text-left"/>
         </v-card>
      </v-container>

    <v-container fluid style="margin: 0px; padding-top: 0px">
      <v-btn-toggle v-model="func_description_toggle" mandatory style="margin: 0px">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small v-bind="attrs" v-on="on">
              <v-icon small>mdi-pound</v-icon>
            </v-btn>
          </template>
          <span>Markdown</span>
      </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small v-bind="attrs" v-on="on">
              <v-icon small>mdi-xml</v-icon>
            </v-btn>
          </template>
          <span>html</span>
      </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small v-bind="attrs" v-on="on">
              <v-icon small>mdi-text-subject</v-icon>
            </v-btn>
          </template>
          <span>Final</span>
      </v-tooltip>
      </v-btn-toggle>
    </v-container>
      <v-row class="pa-3" justify="left" no-gutters v-show="examples_visible">
          <v-col justify="start">


              <v-dialog v-model="examples_editor_open" width="600">
              <template #activator="{ on: dialog }">

                  <v-tooltip right>
                     <template #activator="{ on: tooltip }">
                       <v-btn class="primary" medium right v-on="{ ...tooltip, ...dialog }">
                         <v-icon>edit</v-icon>
                         <span>Examples</span>
                      </v-btn>
                     </template>
                    <span>Add or edit examples (optional)</span>
                  </v-tooltip>

              </template>

              <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                  Examples
                </v-card-title>

                <v-card-text>
                  Edit examples here
                </v-card-text>

                <v-divider></v-divider>

                <v-container fluid v-show="examples_visible">
                <div v-for="(example, index) in examples_and_descriptions">
                  <v-row no-gutters style="height: 50px;" justify="space-around" align="center" dense>
                    <v-col>
                    <v-subheader class="pa-1">Example {{index + 1}}</v-subheader>
                    </v-col>
                    <v-col pa="1" cols="1" sm="2" md="1" lg="1" offset="0" class="text-right">
                      <v-tooltip right>
                         <template v-slot:activator="{ on, attrs }">
                           <v-btn @click="delete_example(index)" v-bind="attrs" v-on="on" fab x-small
                                  flat top :disabled="(examples_and_descriptions.length < 2)"
                                  outlined
                                  style="background-color: #F6F6F6; color: #007960; outline: black"
                           >
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                         </template>
                        <span>Delete example</span>
                      </v-tooltip>
                    </v-col>
                 </v-row>

                  <v-row no-gutters>
                    <v-col fluid v-show="examples_visible">
                      <v-textarea
                          name= "index"
                          clearable
                          clear-icon="mdi-close-circle"
                          label="Type example formula here"
                          auto-grow
                          outlined
                          :value="example.formula"
                          v-model="example.formula"
                          clearable
                          clear-icon="mdi-close-circle"
                          rows="2"
                      ></v-textarea>
                      <v-textarea
                          name= "example.description"
                          clearable
                          clear-icon="mdi-close-circle"
                          label="Type example description here"
                          auto-grow
                          outlined
                          :value="example.description"
                          v-model="example.description"
                          clearable
                          clear-icon="mdi-close-circle"
                          rows="2"
                      ></v-textarea>
                    </v-col>


      </v-row>

    </div>
    </v-container>
                    <v-row class="pa-3" justify="left" no-gutters>
                        <v-col cols="6" sm="4" md='2' offset="0.2">
                          <v-tooltip right>
                             <template v-slot:activator="{ on, attrs }">
                               <v-btn @click="add_example" class="primary" v-bind="attrs" v-on="on" small right :disabled="!add_example_active">
                                 <v-icon>mdi-plus</v-icon>
                                 <span>New Example</span>
                              </v-btn>
                             </template>
                            <span>Add a new example</span>
                          </v-tooltip>

                        </v-col>
      </v-row>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn class="primary"
                    text
                    @click="examples_editor_open = false"
                  >
                    Done
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-col>
      </v-row>
   </v-card>

</template>

