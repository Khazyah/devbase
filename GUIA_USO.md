# 🚀 Guia de Uso - Media Downloader com Progress Bar

## 📋 Pré-Requisitos

- Python 3.8+
- Dependências instaladas (`pip install -r requirements.txt`)

```bash
pip install flet yt-dlp Pillow
```

## 🎮 Como Usar

### Passo 1: Executar o App
```bash
python src/main.py
```

A aplicação abrirá em `http://localhost:8550`

### Passo 2: Fazer um Download

1. **Colar URL**: Cole a URL do vídeo (YouTube, Vimeo, etc) no campo "Your media URL..."
   - Exemplo: `https://www.youtube.com/watch?v=...`

2. **Selecionar Pasta**: Clique no ícone 📁 para escolher onde salvar
   - Versão anterior: clique em "Selecionar Pasta"

3. **Escolher Formato**:
   - `mp4` - Vídeo (mantém vídeo + áudio)
   - `mp3` - Apenas áudio em MP3
   - `wav` - Apenas áudio em WAV

4. **Escolher Qualidade** (só para MP4):
   - `1080p` - Full HD
   - `720p` - HD
   - `360p` - SD
   - `120p` - Muito baixa

5. **Clicar "Download"**:
   - Botão fica desabilitado enquanto valida
   - Abre a barra de progresso
   - Botão muda para "Cancelar"

### Passo 3: Acompanhar Progresso

Enquanto o download acontece, você vê:
- **Barra visual** azul preenchendo
- **Porcentagem**: `45.3%`
- **Bytes baixados**: `150.5MB / 335.2MB`
- **Velocidade**: `2.5MB/s`

### Passo 4: Conclusão

- ✅ **Sucesso**: "✅ Sucesso! Vídeo baixado."
- ❌ **Erro**: "❌ Erro no download: [detalhes]"
- ⚠️ **Cancelado**: "⚠️ Cancelando..."

A UI reseta automaticamente após 2 segundos.

---

## 🛑 Cancelar Download

A qualquer momento durante o download:
1. Clique no botão **"Cancelar"** (vermelho)
2. Download será interrompido
3. Arquivo parcial será deletado pelo yt-dlp
4. Mensagem aparecerá em laranja

---

## ❌ Tratamento de Erros

### Erro: "URL não pode estar vazia"
- **Causa**: Você tentou fazer download sem URL
- **Solução**: Coloque uma URL válida

### Erro: "Selecione uma pasta para salvar"
- **Causa**: Nenhuma pasta foi selecionada
- **Solução**: Clique em 📁 e escolha uma pasta

### Erro: "URL inválida"
- **Causa**: URL não é suportada pelo yt-dlp
- **Solução**: Verifique se é YouTube, Vimeo, etc

### Erro: "Caminho inválido"
- **Causa**: A pasta selecionada não existe mais
- **Solução**: Selecione outra pasta

### Download bem começa mas "congela"
- **Causa**: Pode ser conexão lenta
- **Verificar**: Monitore a velocidade mostrada
- **Solução**: Cancele e tente novamente

---

## 📊 Exemplo de Uso Real

```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Formato: mp4
Qualidade: 720p
Pasta: C:\Videos

[Clica Download]

Progresso aparece:
0% - 0B/345.5MB (Calculando...)
5% - 17.3MB/345.5MB (1.2MB/s)
10% - 34.6MB/345.5MB (1.5MB/s)
20% - 69.1MB/345.5MB (1.8MB/s)
50% - 172.8MB/345.5MB (2.1MB/s)
75% - 259.1MB/345.5MB (2.2MB/s)
100% - Download concluído, processando áudio...

✅ Sucesso! Vídeo baixado.

[Aguarda 2 segundos]

[UI reseta - pronto para novo download]
```

---

## ⚙️ Configurações

### Qualidade de Áudio (Automática)
- **MP3**: 320 kbps (máxima qualidade)
- **WAV**: 192 kbps (para não ficar muito pesado)

### Velocidade de Atualização
- Progress bar atualiza a cada frame do yt-dlp
- Normalmente a cada 100-500ms

### Tempo de Reset
- Após conclusão, aguarda 2 segundos
- Depois reseta botão e progresso

---

## 🔍 Troubleshooting

### App não inicia
```bash
# Verifique Python
python --version

# Reinstale dependências
pip install --upgrade -r requirements.txt

# Limpe cache
python src/main.py  # Na primeira vez pode demorar
```

### Download muito lento
- Verifique sua conexão
- YouTube/Vimeo pode estar throttling
- Tente qualidade menor (360p ao invés de 1080p)

### Botão não volta a ficar ativo
- Aguarde 2 segundos
- Se não voltar, reinicie a aplicação

### Arquivo não aparece na pasta
- Verifique se o download completou (barra 100%)
- Verifique se tem espaço em disco
- Tente baixar em pasta diferente

---

## 🎯 Fluxo de UI

```
┌─────────────────────────────────────┐
│      Media Downloader               │
└─────────────────────────────────────┘
          ↓
    [URL Input Field]
          ↓
┌─────────────────────────────────────┐
│  [Download] [📁] [mp4] [1080p]      │
└─────────────────────────────────────┘

APÓS CLICAR DOWNLOAD:

┌─────────────────────────────────────┐
│      [████████░░░░░░░░░░]  45.3%    │
│    150.5MB / 335.2MB - 2.5MB/s      │
│  [Cancelar]                         │
└─────────────────────────────────────┘

APÓS CONCLUSÃO:

┌─────────────────────────────────────┐
│   ✅ Sucesso! Vídeo baixado.        │
│                                     │
│  [Download] [📁] [mp4] [1080p]      │
└─────────────────────────────────────┘
```

---

## 🎬 URLs Testadas

Essas URLs funcionam bem com o app:

- ✅ YouTube: `https://www.youtube.com/watch?v=...`
- ✅ Vimeo: `https://vimeo.com/...`
- ✅ DailyMotion: `https://www.dailymotion.com/video/...`
- ✅ Spotify: `https://open.spotify.com/...` (áudio)
- ✅ SoundCloud: `https://soundcloud.com/...` (áudio)

---

## 📝 Notas Importantes

1. **Respeite copyright**: Apenas baixe conteúdo que você tem permissão
2. **Armazenamento**: Vídeos em Full HD podem ocupar vários GB
3. **Formato MP4**: Combina melhor vídeo + melhor áudio automaticamente
4. **Cancelamento**: É instantâneo, mas pode levar alguns segundos para parar completamente
5. **Threads**: Não são persistidas entre execuções (cada app é novo)

---

## 🆘 Suporte

Se algo não funcionar:
1. Verifique se todas as dependências estão instaladas
2. Tente com URL diferente
3. Reinicie a aplicação
4. Verifique se tem conexão com internet
5. Verifique logs no console (F12 em navegador)

---

## ✨ Recursos Futuros

Em desenvolvimento:
- [ ] Fila de downloads (QUEUE)
- [ ] Pausar/Resumir
- [ ] Histórico de downloads
- [ ] Converter vídeos após download
- [ ] Tema escuro/claro
- [ ] Notificações

Sugestões? Abra uma issue! 🎉
