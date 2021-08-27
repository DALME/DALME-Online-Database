import * as yup from "yup";

// key, title, itemType, creators, date, detail
// Zotero keys link to these -> Library detail, just render a blob for now
// {
//     "key": "M24MI6RY",
//     "version": 753,
//     "itemType": "bookSection",
//     "title": "Usury, Jewish Law",
//     "creators": [
//         {
//             "creatorType": "author",
//             "firstName": "Haym",
//             "lastName": "Soloveitchik"
//         }
//     ],
//     "abstractNote": "",
//     "bookTitle": "Collected Essays: Volume I",
//     "series": "The Littman Library of Jewish Civilization",
//     "seriesNumber": "",
//     "volume": "1",
//     "numberOfVolumes": "3",
//     "edition": "",
//     "place": "Liverpool",
//     "publisher": "Liverpool University Press",
//     "date": "2013",
//     "pages": "41-43",
//     "language": "English",
//     "ISBN": "",
//     "shortTitle": "",
//     "url": "",
//     "accessDate": "",
//     "archive": "",
//     "archiveLocation": "",
//     "libraryCatalog": "",
//     "callNumber": "",
//     "rights": "",
//     "extra": "",
//     "tags": [],
//     "collections": [],
//     "relations": {},
//     "dateAdded": "2021-07-12T13:34:30Z",
//     "dateModified": "2021-07-12T13:35:06Z"
// }

export const libraryListSchema = yup.array().of(
  yup
    .object()
    .shape({
      key: yup.string().required(),
      title: yup.string().required(),
      itemType: yup.string().required(),
      date: yup.number().required(),
      creators: yup.array().of(
        yup.object().shape({
          creatorType: yup.string().required(),
          firstName: yup.string().required(),
          lastName: yup.string().required(),
        }),
      ),
    })
    .camelCase(),
);
