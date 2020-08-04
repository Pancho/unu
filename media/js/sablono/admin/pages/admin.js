import { BoxComponent } from '../../components/box.js';
import { FieldComponent } from '../../components/field.js';
import { FormComponent } from '../../components/form.js';
import { GridComponent } from '../../components/grid.js';
import { TableComponent } from '../../components/table.js';
import { Component } from '../../fiu/component.js';

export class AdminPageComponent extends Component {
	static tagName = 'admin-page';
	static template = 'components/admin-page';
	static stylesheets = [
		'meta',
		'palette',
		'main',
		'font-awesome',
		'normalize',
		'components/admin-page',
	];
	static registerComponents = [
		TableComponent,
		BoxComponent,
		GridComponent,
		FormComponent,
		FieldComponent,
	];
	static dateTimeFormat = new Intl.DateTimeFormat('en-UK', {
		year: 'numeric',
		month: 'numeric',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
		second: 'numeric',
	});

	articleTable;
	articleForm;

	constructor() {
		super(AdminPageComponent);
		console.log('AdminPageComponent constructor finished');
	}

	onTemplateLoaded() {
		this.initArticleForm();
		this.loadArticles();
	}

	populateFields() {
		return {
			articleTable: '#article-table',
			articleForm: '#article-form',
		};
	}

	initArticleForm() {
		this.articleForm.setFieldTranslations({
			'title': 'article-title',
			'category': 'article-category',
			'content': 'article-content',
			'order': 'article-order',
			'id': 'article-id',
			'article-title': 'title',
			'article-category': 'category',
			'article-content': 'content',
			'article-order': 'order',
			'article-id': 'id',
		});
		this.articleForm.setSuccessHandler(response => {
			if (response.status === 'ok') {
				this.loadArticles();
			} else {
				this.articleForm.setErrors(response.errors);
			}
		});
	}

	loadArticles() {
		this.app.http.get('/article-list').then(response => response.json()).then(response => {
			const data = [];

			response.articles.forEach((article, index) => {
				const editButton = this.newElement('a'),
					deleteButton = this.newElement('a');

				editButton.classList.add('delete', 'button', 'button-small', 'bg-blue-50', 'bg-blue-60-hover');
				editButton.setAttribute('title', 'Edit article');
				editButton.addEventListener('click', event => {
					event.preventDefault();
					this.articleForm.populateForm(article);
				});
				editButton.textContent = 'Edit';

				deleteButton.classList.add('delete', 'button', 'button-small', 'bg-red-50', 'bg-red-60-hover');
				deleteButton.setAttribute('title', 'Delete article');
				deleteButton.addEventListener('click', event => {
					const formData = new FormData(),
						row = event.target.closest('tr');

					event.preventDefault();
					formData.append('id', article.id);
					this.app.http.post('/article-delete', formData)
						.then(response => response.json())
						.then(response => {
							if (response.status === 'ok') {
								row.parentElement.removeChild(row);
							}
						});
				});
				deleteButton.textContent = 'Delete';

				data.push([
					article.title,
					AdminPageComponent.dateTimeFormat.format(new Date(article.published)),
					AdminPageComponent.dateTimeFormat.format(new Date(article.updated)),
					[editButton, deleteButton],
				]);
			});

			this.articleTable.updateBody(data);
		});
	}
}
