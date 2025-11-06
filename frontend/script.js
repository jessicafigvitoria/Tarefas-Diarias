const API_URL = "http://127.0.0.1:8000";

let tarefasGlobais = [];
let tarefaSelecionada = null;

async function carregarTarefas() {
  const res = await fetch(`${API_URL}/tarefas/`);
  const tarefas = await res.json();
  tarefasGlobais = tarefas;
  const lista = document.getElementById("listaTarefas");
  lista.innerHTML = "";

  document.getElementById("contador").textContent = `Total de tarefas: ${tarefas.length}`;

  tarefas.reverse().forEach(t => {
    const li = document.createElement("li");
    li.textContent = `${t.titulo} - ${t.descricao}`;
    if (t.concluida) li.classList.add("concluida");

    li.addEventListener("click", () => abrirModal(t));

    lista.appendChild(li);
  });
}

async function adicionarTarefa() {
  const titulo = document.getElementById("tituloTarefa").value.trim();
  const descricao = document.getElementById("descricaoTarefa").value.trim();
  if (!titulo) return;

  await fetch(`${API_URL}/tarefas/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo, descricao })
  });

  document.getElementById("tituloTarefa").value = "";
  document.getElementById("descricaoTarefa").value = "";
  carregarTarefas();
}

const modal = document.getElementById("modal");
const modalTitulo = document.getElementById("modalTitulo");
const modalDescricao = document.getElementById("modalDescricao");
const btnConcluir = document.getElementById("btnConcluir");
const btnDeletar = document.getElementById("btnDeletar");
const spanClose = document.querySelector(".close");

function abrirModal(tarefa) {
  tarefaSelecionada = tarefa;
  modalTitulo.textContent = tarefa.titulo;
  modalDescricao.textContent = tarefa.descricao;
  btnConcluir.textContent = tarefa.concluida ? "Desmarcar" : "Concluir";
  modal.style.display = "flex";
}

spanClose.onclick = () => { modal.style.display = "none"; }
window.onclick = (event) => { if(event.target === modal) modal.style.display = "none"; }

btnConcluir.onclick = async () => {
  await fetch(`${API_URL}/tarefas/${tarefaSelecionada.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ concluida: !tarefaSelecionada.concluida })
  });
  modal.style.display = "none";
  carregarTarefas();
};

btnDeletar.onclick = async () => {
  await fetch(`${API_URL}/tarefas/${tarefaSelecionada.id}`, { method: "DELETE" });
  modal.style.display = "none";
  carregarTarefas();
};

document.getElementById("btnAdd").addEventListener("click", adicionarTarefa);
window.addEventListener("load", carregarTarefas);
