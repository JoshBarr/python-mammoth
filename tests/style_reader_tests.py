from nose.tools import istest, assert_equal

from mammoth import html_paths, document_matchers, documents, styles
from mammoth.style_reader import read_html_path, read_document_matcher, read_style


@istest
class ReadHtmlPathTests(object):
    @istest
    def can_read_single_element(self):
        assert_equal(
            html_paths.path([html_paths.element(["p"])]),
            read_html_path("p")
        )
    
    @istest
    def can_read_choice_of_two_elements(self):
        assert_equal(
            html_paths.path([html_paths.element(["ul", "ol"])]),
            read_html_path("ul|ol")
        )

    
    @istest
    def can_read_choice_of_three_elements(self):
        assert_equal(
            html_paths.path([html_paths.element(["ul", "ol", "p"])]),
            read_html_path("ul|ol|p")
        )

    
    @istest
    def can_read_nested_elements(self):
        assert_equal(
            html_paths.path([html_paths.element(["ul"]), html_paths.element(["li"])]),
            read_html_path("ul > li")
        )

    
    @istest
    def can_read_class_on_element(self):
        assert_equal(
            html_paths.path([html_paths.element(["p"], class_names=["tip"])]),
            read_html_path("p.tip")
        )

    
    @istest
    def can_read_multiple_classes_on_element(self):
        assert_equal(
            html_paths.path([html_paths.element(["p"], class_names=["tip", "help"])]),
            read_html_path("p.tip.help")
        )

    
    @istest
    def can_read_when_element_must_be_fresh(self):
        assert_equal(
            html_paths.path([html_paths.element(["p"], fresh=True)]),
            read_html_path("p:fresh")
        )


@istest
class ReadDocumentMatcherTests(object):
    @istest
    def reads_plain_paragraph(self):
        assert_equal(
            document_matchers.paragraph(),
            read_document_matcher("p")
        )
    
    
    @istest
    def reads_paragraph_with_style_name(self):
        assert_equal(
            document_matchers.paragraph(style_name="Heading1"),
            read_document_matcher("p.Heading1")
        )
    
    
    @istest
    def reads_paragraph_ordered_list(self):
        assert_equal(
            document_matchers.paragraph(numbering=documents.numbering_level(1, is_ordered=True)),
            read_document_matcher("p:ordered-list(2)")
        )
    
    
    @istest
    def reads_paragraph_unordered_list(self):
        assert_equal(
            document_matchers.paragraph(numbering=documents.numbering_level(1, is_ordered=False)),
            read_document_matcher("p:unordered-list(2)")
        )
    
    
    @istest
    def reads_plain_run(self):
        assert_equal(
            document_matchers.run(),
            read_document_matcher("r")
        )
    
    
    @istest
    def reads_run_with_style_name(self):
        assert_equal(
            document_matchers.run(style_name="Emphasis"),
            read_document_matcher("r.Emphasis")
        )


@istest
def document_matcher_is_mapped_to_html_path_using_fat_arrow():
    assert_equal(
        styles.style(document_matchers.paragraph(), html_paths.path([html_paths.element(["h1"])])),
        read_style("p => h1")
    )
