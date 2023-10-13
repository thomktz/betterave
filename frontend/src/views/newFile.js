import axios from 'axios';

export default (await import('vue')).defineComponent({
components: {
StudentCalendar,
ProfilePill,
InfoColumn,
ColumnNextclasses,
},
data() {
return {
user: {
name: '',
email: ''
},
//upcomingClasses: nextClasses.map((course) => ({id: course.id, text: course.name,color: course.color,})),
nextClasses: [],
homeworkList: [{ id: 1, text: "Algebra homework" }, { id: 2, text: "Essay on WW2" }],
notifications: [{ id: 1, text: "Meeting tomorrow" }, { id: 2, text: "Homework due" }]
};
},
async mounted() {
try {
const response = await axios.get('http://127.0.0.1:5000/profile', { withCredentials: true });
this.user = response.data;
this.$emit('updateTitle', "Hello, " + this.user.name + "!");

const allClasses = await axios.get('http://127.0.0.1:5000/lessons', { withCredentials: true });
const currentTime = new Date();
this.nextClasses = allClasses.data.filter((course) => new Date(course.start) > currentTime).slice(0, 5).map(course => ({
id: course.id,
text: course.title,
start: course.start,
end: course.end,
color: course.color,
}));
//this.nextClasses = nextClasses.slice(0, 5); // Limitez à 5 prochains cours
//this.nextClasses = nextClasses.map((course) => ({id: course.id, text: course.name,color: course.color,}))
} catch (error) {
console.error("There was an error fetching user data:", error);
}
},
methods: {}
});
