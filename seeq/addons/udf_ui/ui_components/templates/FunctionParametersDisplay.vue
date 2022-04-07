<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="parameters_visible?'background-color:#F6F6F6; opacity: 1; min-width: 300px': 'display: none !important'"
  >
    <v-card-title>
      {{class_functionality}}
    </v-card-title>

    <v-container>

      <div v-for="(param, index) in params_and_types" :key="param.name">
        <v-row no-gutters style="height: 50px;" justify="space-around" align="center" dense>
          <v-col cols="1" sm="4" md="4" lg="4" offset="0">
            <v-text-field
                label="Parameter Name"
                @change="update_param([$event, index, 'name'])"
                :value="param.name" :rules="[v => !!v || 'Parameter name required']">
            </v-text-field>
          </v-col>

          <v-col cols="1" sm="4" md="4" lg="4" offset="1">
            <v-select
                label="Parameter Type"
                @change="update_param([$event, index, 'type'])"
                :items=params_options v-model="param.type"
                :value="param.type">
            </v-select>
          </v-col>

          <v-col cols="1" sm="2" md="1" lg="1" offset="1">
            <v-tooltip right>
               <template v-slot:activator="{ on, attrs }">
                 <v-btn @click="delete_param(index)" class="primary" v-bind="attrs" v-on="on"
                        x-small fab min-width="10px" width="30px" min-height="10px" height="30px"
                        middle :disabled="(params_and_types.length < 2)"
                 >
                  <v-icon>close</v-icon>
                </v-btn>
               </template>
              <span>Delete parameter</span>
            </v-tooltip>

          </v-col>

          <v-col pa="1" cols="1" sm="2" md="1" lg="1" offset="0" style="justify-content:flex-end; display: flex">
            <v-tooltip right>
               <template v-slot:activator="{ on, attrs }">
                  <v-btn @click="use_param_in_formula(index)" class="primary" v-bind="attrs" v-on="on"
                         x-small fab min-width="10px" width="30px" min-height="10px" height="30px"
                         middle :disabled="!avail_active"
                  >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
               </template>
              <span>Use in formula</span>
            </v-tooltip>

          </v-col>

        </v-row>
      </div>
      <v-spacer style="height: 20px;"></v-spacer>

      <v-row class="pa-0" justify="left">
          <v-col justify="start">
            <v-tooltip right>
               <template v-slot:activator="{ on, attrs }">
                 <v-btn @click="add_param" class="primary" v-bind="attrs" v-on="on" small right :disabled="!add_active">
                   <v-icon>mdi-plus</v-icon>
                   <span>New parameter</span>
                </v-btn>
               </template>
              <span>Add a new parameter</span>
            </v-tooltip>
          </v-col>

          <v-col style="justify-content:flex-end; display: flex">
            <v-dialog v-model="parse_dialog_open" width="600" scrollable>
              <template #activator="{ on: dialog }">
                  <v-tooltip right>
                     <template #activator="{ on: tooltip }">
                       <v-btn class="primary" medium right v-on="{ ...tooltip, ...dialog }" :disabled="!formula" @click="parse_dialog_open = true" small right>
                         <v-icon>mdi-calculator-variant</v-icon>
                         <span>Parse Formula</span>
                      </v-btn>
                     </template>
                    <span>Obtain parameters from the formula</span>
                  </v-tooltip>

              </template>

            <v-card>
              <v-card-title class="text-h5 grey lighten-2">
                Parse Formula
              </v-card-title>

              <v-card-text style="color: dimgrey" >
                <span>Extracting parameters form the formula will override the existing parameters list. Automatically-extracted parameters
                  inherently may be erroneous and should be verified manually. The type is set to signal for all obtained parameters.</span>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                      <v-btn text @click="parse_dialog_open = false" outlined="true"
                             style="background-color: #F6F6F6; color: black; outline: black">
                        <v-icon>mdi-close</v-icon>
                        <span>Cancel</span>

                      </v-btn>
                      <v-btn class="primary" text @click="parse_dialog_open = false" @click="parse_on_click">
                        <v-icon>done</v-icon>
                        <span>Parse</span>
                      </v-btn>

              </v-card-actions>
            </v-card>
            </v-dialog>
          </v-col>

      </v-row>
    </v-container>

    <v-container fluid v-show="parameters_visible" >
      <v-textarea
        name="formula"
        label="Type the formula here"
        outlined
        :value="formula"
        v-model="formula"
        clear-icon="mdi-close-circle"
        height="490"
        dense
        style="font-size: 15px;"
        no-resize="true"
        wrap="off"
      ></v-textarea>

    </v-container>

  </v-card>

</template>


