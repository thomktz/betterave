<template>
  <v-dialog v-model="dialog" persistent max-width="500px">
    <v-card>
      <v-card-title class="headline">Register</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                label="First Name"
                v-model="name"
                placeholder="John"
                :rules="nameRules"
                required
                prepend-icon="mdi-account"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                label="Last Name"
                placeholder="Doe"
                v-model="surname"
                :rules="surnameRules"
                required
                prepend-icon="mdi-account-outline"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                label="Email"
                v-model="email"
                disabled
                prepend-icon="mdi-email"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                label="Password"
                v-model="password"
                type="password"
                :rules="passwordRules"
                required
                prepend-icon="mdi-lock"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-select
                label="Level"
                :items="['1A', '2A', '3A']"
                v-model="level"
                required
                prepend-icon="mdi-school"
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-row align="start" no-gutters>
                <v-col cols="auto">
                  <v-checkbox
                    class="gdpr-checkbox"
                    v-model="gdprConsent"
                    :rules="[v => v || 'You must agree to continue']"
                    required
                  ></v-checkbox>
                </v-col>
                <v-col cols="auto" class="checkbox-label">
                  I agree to the
                  <span 
                    class="gdpr-link" 
                    @click="openGdprDialog"
                    role="button"
                    tabindex="0"
                    style="text-decoration: underline; color: #1976D2; cursor: pointer;">
                    GDPR terms.
                  </span>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="register">Register</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-dialog v-model="showGdprDialog" persistent max-width="800px">
    <v-card>
      <v-card-title class="headline">GDPR Compliance Information</v-card-title>
      <v-card-text>
        <div class="gdpr-text">{{ gdprTextContent }}</div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" text @click="showGdprDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script>
import { apiClient, toast } from "@/apiConfig";

export default {
  data() {
    return {
      dialog: false,
      name: "",
      surname: "",
      email: "",
      password: "",
      level: "",
      nameRules: [
        (v) => !!v || "Name is required",
        (v) => (v && v.length >= 2) || "Name must be at least 2 characters",
        (v) => (v && v.length <= 20) || "Name must be less than 20 characters",
        (v) =>
          /^[A-Z][a-z]*$/.test(v) ||
          "First letter must be capitalized, others lowercase",
      ],
      surnameRules: [
        (v) => !!v || "Surname is required",
        (v) => (v && v.length >= 2) || "Surname must be at least 2 characters",
        (v) =>
          (v && v.length <= 20) || "Surname must be less than 20 characters",
        (v) =>
          /^[A-Z][a-z]*$/.test(v) ||
          "First letter must be capitalized, others lowercase",
      ],
      passwordRules: [
        (v) => !!v || "Password is required",
        (v) => (v && v.length >= 4) || "Password must be at least 4 characters",
      ],
      gdprConsent: false,
      showGdprChart: false,
      gdprTextContent: '',
      showGdprDialog: false, 
    };
  },
  watch: {
    name(newVal) {
      this.updateEmail();
    },
    surname(newVal) {
      this.updateEmail();
    },
  },
  methods: {
    updateEmail() {
      const formattedName = this.name.toLowerCase().replace(/ /g, "-");
      const formattedSurname = this.surname.toLowerCase().replace(/ /g, "-");
      this.email = `${formattedName}.${formattedSurname}@ensae.fr`;
    },
    open() {
      this.dialog = true;
    },
    close() {
      this.name = "";
      this.surname = "";
      this.email = "";
      this.password = "";
      this.level = "";

      this.dialog = false;
    },
    async register() {
      try {
        const response = await apiClient.post("/users/", {
          name: this.name,
          surname: this.surname,
          profile_pic: "default_profile_pic.png",
          user_type: "student",
          level: this.level,
          email_override: this.email,
          password_override: this.password,
        });

        toast.success("User created successfully");
        this.close();
      } catch (error) {
        console.error("Error creating user:", error);
      }
    },
    async fetchGdprContent() {
      const response = await fetch('/gdpr-policy.txt');
      if (response.ok) {
        const text = await response.text();
        this.gdprTextContent = text;
      } else {
        console.error('Failed to load GDPR content');
        this.gdprTextContent = 'Failed to load content. Please try again later.';
      }
    },
    openGdprDialog() {
      this.fetchGdprContent();
      this.showGdprDialog = true;
    }
  },
};
</script>

<style scoped>
.checkbox-label {
  margin-top: 15px;
}
.gdpr-text {
  white-space: pre-wrap;
  font-family: 'Arial', sans-serif;
}
.gdpr-link {
  text-decoration: underline;
  color: #1976D2;
  cursor: pointer;
}
.gdpr-checkbox {
  width: 90px;
}
</style>
