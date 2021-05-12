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
      :data="pagedTickets"
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
      <h5 class="subheading">
        {{ ticketCount }}{{ ticketCount === 1 ? " issue" : " issues" }}
      </h5>
      <el-pagination
        :current-page="pageNumber"
        :page-size="pageSize"
        :small="paginationStyle"
        :total="ticketCount"
        layout="prev, pager, next"
        hide-on-single-page
        @current-change="handleCurrentChange"
      >
      </el-pagination>
    </el-container>
  </el-card>
</template>

<script>
import { computed, inject, reactive, toRefs } from "vue";
import { useStore } from "vuex";

import { API } from "@/api";
import { ticketListSchema } from "@/schemas";
import { useFilter, usePagination } from "@/use";

export default {
  name: "Tickets",
  async setup() {
    const store = useStore();
    const $mq = inject("mq");
    const state = reactive({
      count: 0,
      pageNumber: 1,
      pageSize: 10,
      q: "",
      tickets: [],
    });

    const userId = store.getters.userId;
    const { success, data } = await API.tickets.userTickets(userId);
    if (success)
      await ticketListSchema
        .validate(data, { stripUnknown: true })
        .then((value) => {
          state.count = value.count;
          state.next = value.next;
          state.previous = value.previous;
          state.tickets = value.results;
        });

    const reducer = (ticket) =>
      ticket.subject.toLowerCase().includes(state.q.toLowerCase());
    const filteredTickets = computed(() => {
      return useFilter(reducer, state.tickets);
    });
    const ticketCount = computed(() => filteredTickets.value.length);

    const pagedTickets = computed(() =>
      usePagination(state.pageNumber, state.pageSize, filteredTickets),
    );

    const cardRules = "{ padding: '0px', margin: '0 2.5%' }";
    const cardStyle = computed(() => ($mq.value === "sm" ? cardRules : "{}"));
    const paginationStyle = computed(() => ($mq.value === "sm" ? true : false));

    return {
      ...toRefs(state),
      cardStyle,
      pagedTickets,
      paginationStyle,
      ticketCount,
    };
  },
  methods: {
    handleCurrentChange(pageNumber) {
      this.pageNumber = pageNumber;
    },
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
