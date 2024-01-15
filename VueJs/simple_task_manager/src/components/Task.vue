<template>
    <div @dblclick="this.$emit('double-click', id)" :class="[task.reminder ? 'reminder' : '', 'task']">
        <h3>
            {{ task.text }}
            <i @click="this.$emit('delete-task', id)"  class="fas fa-times"></i>
        </h3>
        <p>{{ task.day }}</p>
    </div>
    
</template>


<script>
    export default {
        name: "Task",
        props: {
            task: Object
        },
        methods: {
        }
    }
</script>

<style scope>
.fas {
  color: red;
}

.task {
  background: #ece2e2;
  margin: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

.task.reminder {
  border-left: 5px solid green;
}

.task h3 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>