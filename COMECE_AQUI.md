# 🚀 COMECE AQUI - Primeira Execução

## Passo 1: Instalar e Rodar

Execute no terminal:

```bash
./iniciar.sh
```

Isso vai:
1. ✅ Criar ambiente virtual Python
2. ✅ Instalar dependências (Flask, SQLAlchemy)
3. ✅ **Popular o banco com TODOS os seus dados reais**
4. ✅ Iniciar o servidor

## Passo 2: Acessar o Sistema

1. Abra o navegador
2. Acesse: **http://localhost:5000**
3. Faça login:
   - **Usuário:** voce
   - **Senha:** senha123

## 📊 Seus Dados Já Estão Cadastrados!

### ✅ Receitas (R$ 8.500,00)
- Entrada 1: R$ 4.600,00
- Entrada 2: R$ 3.900,00

### ✅ Despesas Fixas (R$ 6.737,51)
**Moradia:**
- Aluguel: R$ 900,00
- Luz: R$ 500,00
- Água: R$ 90,00
- Internet: R$ 110,00
- Faxina: R$ 500,00

**Transporte:**
- Passagem: R$ 150,00
- Carona: R$ 150,00

**Criança:**
- Plano de saúde: R$ 331,00
- Escola: R$ 600,00
- Fraldas: R$ 150,00
- Medicamentos: R$ 100,00
- Roupas: R$ 150,00
- Passeios: R$ 200,00

**Pet (Cachorro):**
- Ração: R$ 100,00
- Sardinhas: R$ 200,00
- Vacinas (reserva): R$ 25,00

**Alimentação:**
- Compras: R$ 1.200,00
- Proteínas: R$ 200,00

**Outros:**
- Corte cabelo: R$ 50,00
- MEI: R$ 160,00
- Roupas adultos: R$ 100,00
- Streamings: R$ 72,70
- Dívidas: R$ 200,00
- Cartão IA: R$ 120,00
- Parcelas PC: R$ 378,81 (3 meses restantes)

### 💰 Saldo Disponível: R$ 1.762,49/mês

## 🎯 O Que Fazer Agora

### 1. Explore o Dashboard
- Veja o resumo das suas finanças
- Confira o progresso da reserva de emergência

### 2. Marque Despesas Como Pagas
- Vá em "Despesas Fixas"
- Clique no checkbox quando pagar cada conta
- Fica verde quando marcado como pago

### 3. Registre Gastos Diários
- Vá em "Gastos Diários"
- Toda vez que gastar algo (mercado, farmácia, etc.)
- Registre imediatamente

### 4. Acompanhe Sua Reserva
- Vá em "Reserva"
- Quando guardar dinheiro, registre
- Meta: R$ 40.500,00 em 30 meses
- Plano: começar com R$ 800/mês

## 👥 Acesso da Esposa

Sua esposa pode fazer login com:
- **Usuário:** esposa
- **Senha:** senha123

Vocês dois veem e editam os mesmos dados!

## 💡 Dicas Importantes

1. **Registre TODO gasto extra** - Não deixe passar nada
2. **Marque despesas pagas** - Ajuda a controlar o que falta
3. **Registre depósitos na reserva** - Acompanhe seu progresso
4. **Use pelo celular** - Acesse de qualquer lugar na mesma rede

## 📱 Acesso pelo Celular

1. Descubra o IP do seu computador:
   ```bash
   ifconfig | grep inet
   ```

2. No celular, acesse:
   ```
   http://SEU_IP:5000
   ```

3. Faça login normalmente!

## 🔄 Próximas Ações

### Esta Semana:
- [ ] Marcar todas as despesas já pagas este mês
- [ ] Registrar gastos extras que já fez
- [ ] Se já guardou dinheiro, registrar na Reserva

### Este Mês:
- [ ] Cancelar 2 streamings (Disney+ e Apple TV) = economia de R$ 37,90
- [ ] Investigar conta de luz alta (meta: reduzir para R$ 350)
- [ ] Guardar R$ 800 na reserva de emergência

### Próximos 3 Meses:
- [ ] Quitar parcelas do computador (libera R$ 378,81)
- [ ] Atingir R$ 2.400 na reserva
- [ ] Aumentar poupança para R$ 1.000/mês

## 🆘 Problemas?

### Erro ao rodar:
```bash
pip install --upgrade pip
pip install -r requirements.txt
python popular_dados.py
python app.py
```

### Quer recomeçar do zero:
```bash
rm financas.db
python popular_dados.py
python app.py
```

## 🎉 Pronto!

Seu sistema está funcionando com todos os seus dados reais.
Agora é só usar no dia a dia e acompanhar suas finanças!

**Boa sorte na jornada para R$ 40.500! 💰🚀**
