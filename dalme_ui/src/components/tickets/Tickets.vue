<template>
  <el-card class="box-card" :body-style="cardStyle">
    <el-container class="header u-flip-orientation">
      <h4 class="subheading">My Issue Tickets</h4>
      <el-input
        v-model="q"
        placeholder="Filter issues"
        prefix-icon="el-icon-search"
        clearable
      >
      </el-input>
    </el-container>
    <el-table
      v-if="tickets"
      :data="filteredTickets"
      :default-sort="{ prop: 'id', order: 'ascending' }"
      :empty-text="'No issues'"
      style="width: 100%"
    >
      <el-table-column prop="id" label="ID" sortable width="auto">
      </el-table-column>
      <el-table-column prop="subject" label="Ticket" sortable>
      </el-table-column>
      <el-table-column prop="commentCount">
        <template #default="scope">
          <span v-if="scope.row.commentCount" class="comments">
            <span class="comment-count">{{ scope.row.commentCount }}</span>
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="tag" label="Tag" sortable> </el-table-column>
    </el-table>
    <el-container class="pagination">
      <h5 class="subheading">{{ countInfo }}</h5>
      <el-pagination
        :total="ticketCount"
        :small="paginationStyle"
        layout="prev, pager, next"
        hide-on-single-page
      >
      </el-pagination>
    </el-container>
  </el-card>
</template>

<script>
import { computed, inject, ref } from "vue";

import { API } from "@/api";
import { ticketListSchema } from "@/schemas";
import { useFilter } from "@/use";

export default {
  name: "Tickets",
  async setup() {
    const $mq = inject("mq");
    const q = ref("");
    const count = ref(null);
    const next = ref(null);
    const previous = ref(null);
    const tickets = ref([]);
    const cardStyle = computed(() =>
      $mq.value === "sm" ? "{ padding: '0px', margin: '0 2.5%' }" : "{}",
    );
    const paginationStyle = computed(() => ($mq.value === "sm" ? true : false));
    const reducer = (ticket) =>
      ticket.subject.toLowerCase().includes(q.value.toLowerCase());
    const filteredTickets = computed(() => {
      return useFilter(reducer, tickets.value);
    });
    const ticketCount = computed(() =>
      q.value ? filteredTickets.value.length : count.value,
    );
    const countInfo = computed(() =>
      ticketCount.value === 1
        ? `${ticketCount.value} issue`
        : `${ticketCount.value} issues`,
    );

    // TODO: const { _, _ } = await API.auth.session();
    const userId = 84;
    const { success, data } = await API.tickets.userTickets(userId);
    if (success)
      ticketListSchema.validate(data, { stripUnknown: true }).then((value) => {
        count.value = value.count;
        next.value = value.next;
        previous.value = value.previous;
        tickets.value = value.results;
      });

    return {
      cardStyle,
      count,
      countInfo,
      filteredTickets,
      paginationStyle,
      q,
      tickets,
      ticketCount,
    };
  },
};
</script>

<style scoped>
.el-container {
  flex-direction: column;
}
.el-input {
  margin: 0 auto;
}
.el-pagination {
  margin-left: 0;
  padding: 0;
}
h4,
h5 {
  align-self: flex-start;
  padding: 0.5rem 0;
}
.comments {
  padding: 0 2rem;
  font-weight: bold;
}
.comment-count {
  display: inline-block;
  font-size: 0.7rem;
}
.header {
  flex-direction: column;
}
.pagination {
  align-items: center;
  display: flex;
  flex-direction: column-reverse;
  margin-top: 1rem;
}
@media screen and (min-width: 600px) {
  .header {
    flex-direction: row;
  }
  .el-input {
    margin: 0 0 0 auto;
    width: 50%;
  }
}
@media screen and (min-width: 720px) {
  .el-pagination {
    margin-left: auto;
  }
  .pagination {
    flex-direction: row;
  }
}
@media screen and (min-width: 960px) {
  .el-input {
    width: 25%;
  }
}
</style>
