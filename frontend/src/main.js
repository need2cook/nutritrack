import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

/* FontAwesome */
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
  faCalendar, 
  faUtensils, 
  faDumbbell, 
  faGlassWater, 
  faPlus,
  faChevronLeft,
  faChevronRight,
  faChevronDown,
  faChevronUp,
  faAppleAlt,
  faTimes,
  faPen,
  faChartPie,
  faFlag,
  faUser 
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faCalendar, 
  faUtensils, 
  faDumbbell, 
  faGlassWater, 
  faPlus, 
  faChevronLeft, 
  faChevronRight, 
  faChevronDown, 
  faChevronUp,
  faAppleAlt, 
  faTimes,
  faPen,
  faChartPie,
  faFlag,
  faUser
)

const app = createApp(App)
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
