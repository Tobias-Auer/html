<template>
    <div :key="task.id" v-for="task in tasks">
        <Task @delete-task="$emit('delete-task', task.id)" @double-click="$emit('double-click', task.id)" :task="task" />
    </div>
</template>


<script>
import Task from "./Task"

export default {
    name: "Tasks",
    components: {
        Task
    },
    props: {
        tasks: Array
    },
    emits: ["delete-task", "double-click"]
}
</script>