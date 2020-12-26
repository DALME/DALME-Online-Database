function zotero_rendering_load() {}

function zotero_rendering_init() {}

function zotero_title(data, type, row, meta) {
  if (typeof data != 'undefined' && data != '') {
    if (typeof row.url != 'undefined' && row.url != '') {
      return `<a href="${row.url}">${data}</a>`
    } else {
      return data
    }
  } else {
    if (typeof row.url != 'undefined' && row.url != '') {
      let url = row.url.substring(0, 55)
      return `${url}...`
    } else {
      return 'Not available'
    }
  }
}

function zotero_creators(data, type, row, meta) {
  result = []
  for (let i = 0, len = data.length; i < len; ++i) {
    let name = ''
    if (data[i].hasOwnProperty('name')) {
      name += data[i]['name']
    } else if (data[i].hasOwnProperty('firstName') && data[i].hasOwnProperty('lastName')) {
      name += `${data[i]['firstName']} ${data[i]['lastName']}`
    }
    if (data[i]['creatorType'] == 'editor') { name += ' (ed.)'}
    result.push(name)
  }
  return result.join(', ')
}

function zotero_detail(data, type, row, meta) {
  if (data == 'journalArticle') {
    return `${row.publicationTitle}, ${row.issue}:${row.pages}`
  } else if (data == 'book') {
    return `${row.publisher}, ${row.place}`
  }
}

function zotero_type(data, type, row, meta) {
  return _.startCase(data)
}
