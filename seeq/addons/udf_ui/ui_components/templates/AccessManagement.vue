<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="access_management_visible?'background-color:#F6F6F6; opacity: 1; min-width: 300px':
      'display: none !important'"
  >
    <v-card-title>
      {{class_functionality}}
    </v-card-title>
    <v-subheader style="height: fit-content; padding-bottom: 15px; font-size: 12px">Applies to the package</v-subheader>
    <v-row class="pa-3" justify="left" no-gutters v-show="access_management_visible">
        <v-col justify="start">
          <v-dialog v-model="access_management_open" width="600">
            <template #activator="{ on: dialog }">
                <v-tooltip right>
                   <template #activator="{ on: tooltip }">
                     <v-btn class="primary" medium right v-on="{ ...tooltip, ...dialog }"
                            @click="initialize_access_list"
                     >
                       <v-icon>supervisor_account</v-icon>
                       <span>Manage Access</span>
                    </v-btn>
                   </template>
                  <span>View or edit permissions (optional)</span>
                </v-tooltip>
            </template>
          <v-card>
            <v-card-title class="text-h5 grey lighten-2">
              Access Control
            </v-card-title>
            <v-card-text>
              Manage who can access the UDF
            </v-card-text>
            <v-divider></v-divider>
            <v-container fluid>
                <v-data-table dense :headers="headers" :items="selected_users_dict" item-key="name"
                              class="elevation-1"
                  >
                  <template v-slot:item.read="{ item }">
                    <v-simple-checkbox
                      v-model="item.read"
                      color="#007960"
                    ></v-simple-checkbox>
                  </template>
                  <template v-slot:item.write="{ item }">
                    <v-simple-checkbox
                      v-model="item.write"
                      color="#007960"
                    ></v-simple-checkbox>
                  </template>
                  <template v-slot:item.manage="{ item }">
                    <v-simple-checkbox
                      v-model="item.manage"
                      color="#007960"
                    ></v-simple-checkbox>
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-tooltip right>
                       <template v-slot:activator="{ on, attrs }">
                         <v-btn @click="delete_user_from_table(item)" v-bind="attrs" v-on="on"
                                x-small fab min-width="0" width="18px" min-height="0" height="18px"
                                :disabled="(selected_users_dict.length < 2)"
                                outlined style="background-color: #F6F6F6; color: #007960; outline: black"
                         >
                          <v-icon>close</v-icon>
                        </v-btn>
                       </template>
                      <span>Remove user or user group access</span>
                    </v-tooltip>
                  </template>
                </v-data-table>
            </v-container>
            <v-spacer></v-spacer>
            <v-container fluid>
                <v-autocomplete v-model="users_name_list_selected" :items="users_name_list_searched"
                    :search-input.sync="search" item-text="Description" item-value="users_name_list"
                    label="Users or user groups" placeholder="Type user or user group name"  chips small-chips
                    outlined multiple @change="update_selected_list" close
                >
                </v-autocomplete>
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn class="primary" text @click="access_management_open = false">
                Done
              </v-btn>
            </v-card-actions>
          </v-card>
          </v-dialog>
        </v-col>
    </v-row>
  </v-card>
</template>
