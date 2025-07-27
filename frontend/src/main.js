import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
// Hapus import themeStore

// PrimeVue imports
import PrimeVue from 'primevue/config'
import 'primeicons/primeicons.css'

// PrimeVue components
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Dialog from 'primevue/dialog'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import Tag from 'primevue/tag'
import Calendar from 'primevue/calendar'
import Checkbox from 'primevue/checkbox'
import Avatar from 'primevue/avatar'
import Badge from 'primevue/badge'
import Menu from 'primevue/menu'
import Tooltip from 'primevue/tooltip'
import Popover from 'primevue/popover'

// Tailwind CSS
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Hapus inisialisasi theme

// Use PrimeVue in unstyled mode
app.use(PrimeVue, {
    unstyled: true
})
app.use(ToastService)

// Register PrimeVue components globally
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Button', Button)
app.component('InputText', InputText)
app.component('Select', Select)
app.component('Dialog', Dialog)
app.component('Toast', Toast)
app.component('Tag', Tag)
app.component('Calendar', Calendar)
app.component('Checkbox', Checkbox)
app.component('Avatar', Avatar)
app.component('Badge', Badge)
app.component('Menu', Menu)
app.component('Popover', Popover)

// Register directives
app.directive('tooltip', Tooltip)

app.mount('#app')