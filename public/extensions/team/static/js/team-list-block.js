class TeamListBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);
        const modeSelect = document.getElementById(`${prefix}-mode`);
        const fields = {
          role: document.querySelector("[data-contentpath=role]"),
          members: document.querySelector("[data-contentpath=members]"),
        }

        const listByRole = document.createElement("div");
        listByRole.classList.add("list-by-role");
        document.querySelector("[data-contentpath=role] .w-field__input").appendChild(listByRole);

        const onRoleChange = () => {
          const role = fields["role"].querySelector("select").value;
          if (role) {
            fetch(`/api/public/team/?roles=${role}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                  listByRole.innerHTML = "";
                  data.forEach((item) => {
                    const entry = document.createElement("div");
                    entry.innerText = item.name;
                    listByRole.appendChild(entry);
                  });
                } else {
                  listByRole.innerHTML = '<div class="role-list-empty">No team members have been assigned this role yet.</div>'
                }
            });
          } else {
            listByRole.innerHTML = "";
          }
        }

        const toggleForm = () => {
          const selValue = modeSelect.value;
          if (selValue) {
            const altMode = selValue == "members" ? "role" : "members";
            fields[selValue].classList.remove("u-none");
            fields[altMode].classList.add("u-none");
            if (selValue == "role") {
              fields["role"].addEventListener("change", onRoleChange);
            }
          } else {
            Object.keys(fields).forEach((key) => fields[key].classList.add("u-none"));
            fields["role"].removeEventListener("change", onRoleChange);
          }
        }

        modeSelect.addEventListener("change", toggleForm);
        toggleForm();
        onRoleChange();

        return block;
    }
}

window.telepath.register('publicteam.TeamListBlock', TeamListBlockDefinition);
