<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="summary_visible?'background-color:#F6F6F6; opacity: 1; height:220px; min-width: 300px':
      'display: none !important'"
  >
    <v-card-title>
      {{class_functionality}}
    </v-card-title>
    <v-subheader style="height: fit-content; padding-bottom: 15px; font-size: 12px">
      Review and submit the changes, or delete the selected UDF
    </v-subheader>

     <v-container>
      <v-row class="pa-1" justify="left" no-gutters v-show="summary_visible">
          <v-col justify="start">
            <v-dialog v-model="summary_open" width="600" scrollable>
              <template #activator="{ on: dialog }">
                  <v-tooltip right>
                     <template #activator="{ on: tooltip }">
                       <v-btn class="primary" medium right v-on="{ ...tooltip, ...dialog }" @click="on_review"
                              :disabled="!(selected_package && selected_function)"
                       >
                         <v-icon>done</v-icon>
                         <span>Review</span>
                      </v-btn>
                     </template>
                    <span>Review and submit changes</span>
                  </v-tooltip>

              </template>

            <v-card>
              <v-card-title class="text-h5 grey lighten-2">
                Submit changes
              </v-card-title>

              <v-card-text style="font-family: Courier; color: dimgrey" >
                    <v-expansion-panels accordion>
                      <v-expansion-panel>
                        <v-expansion-panel-header style="font-family: Arial; color: black">
                          Review the details
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                          <div><strong style="font-family: Arial; color: dimgrey">Action:</strong> {{ action }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Package:</strong> {{ selected_package }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Function:</strong> {{ selected_function }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Parameters:</strong> {{ params_and_types }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Formula:</strong> {{ formula }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Function Description:</strong> {{ func_description }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Package Description:</strong> {{ package_description }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Examples:</strong> {{ examples_and_descriptions }}</div>
                          <div><strong style="font-family: Arial; color: dimgrey">Access Control:</strong> {{ selected_users_dict }}</div>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                    </v-expansion-panels>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text @click="summary_open = false" outlined
                style="background-color: #F6F6F6; color: black; outline: black"
                >
                  <v-icon>mdi-close</v-icon>
                  Cancel
                </v-btn>
                <v-btn class="primary" text @click="summary_open = false" @click="on_submit">
                  <v-icon>done</v-icon>
                  Submit
                </v-btn>
              </v-card-actions>
            </v-card>
            </v-dialog>
          </v-col>
          <v-col style="justify-content:flex-end; display: flex">
            <v-dialog v-model="delete_open" width="600" scrollable>
              <template #activator="{ on: dialog }">
                  <v-tooltip right>
                     <template #activator="{ on: tooltip }">
                       <v-btn medium right v-on="{ ...tooltip, ...dialog }"  @click="update_delete_choices"
                              style="background-color: firebrick; color: white"
                              :disabled="!(selected_package || selected_function)"
                       >
                         <v-icon>delete</v-icon>
                         <span>Delete</span>
                      </v-btn>
                     </template>
                    <span>Archive function or package</span>
                  </v-tooltip>

              </template>

            <v-card>
              <v-card-title class="text-h5 grey lighten-2">
                Archive function or package
              </v-card-title>

              <v-card-text style="font-family: Courier; color: dimgrey" >
                        <v-select
                        :items="delete_choices"
                        label="Select object"
                        v-model="selected_for_delete"
                      ></v-select>

              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text @click="delete_open = false" outlined
                style="background-color: #F6F6F6; color: black; outline: black"
                >
                  <v-icon>mdi-close</v-icon>
                  Cancel
                </v-btn>
                <v-btn @click="delete_open = false" @click="on_delete" :disabled="!selected_for_delete"
                       style="background-color: firebrick; color: white"
                >
                  <v-icon>mdi-delete</v-icon>
                  Delete
                </v-btn>
              </v-card-actions>

            </v-card>
            </v-dialog>
          </v-col>
      </v-row>

    </v-container>
  </v-card>
</template>


