# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2016-2019 by the contributors (see AUTHORS file).
    :license: BSD-2-Clause, see LICENSE for details.
"""

from .builder import ConfluenceBuilder
from .directives import JiraDirective
from .directives import JiraIssueDirective
from .logger import ConfluenceLogger
from .nodes import jira
from .nodes import jira_issue
from .translator import ConfluenceTranslator
from .util import ConfluenceUtil
from docutils import nodes
from pkg_resources import parse_version
from sphinx.__init__ import __version__ as sphinx_version
from sphinx.writers.text import STDINDENT
import argparse
import os

# load autosummary extension if available to add additional nodes
try:
    from sphinx.ext import autosummary
except ImportError:
    pass

# load imgmath extension if available to handle math configuration options
try:
    from sphinx.ext import imgmath
except:
    imgmath = None

__version__='1.2.0-dev0'

def main():
    parser = argparse.ArgumentParser(prog=__name__,
        description='Sphinx extension to output Atlassian Confluence content.')
    parser.add_argument(
        '--version', action='version', version='%(prog)s ' + __version__)

    parser.parse_args()
    parser.print_help()
    return 0

def setup(app):
    ConfluenceLogger.initialize()

    app.require_sphinx('1.0')
    app.add_builder(ConfluenceBuilder)
    app.registry.add_translator(ConfluenceBuilder.name, ConfluenceTranslator)

    # sphinx v1.6 is deprecated and is planned to be dropped in v1.3+
    # (ignore when tox is running; TOX_WORK_DIR)
    if (parse_version(sphinx_version) < parse_version('1.7') and not
            'TOX_WORK_DIR' in os.environ):
        ConfluenceLogger.warn('(deprecated) builder {} deprecated for '
            'Sphinx v1.6 and older'.format(ConfluenceBuilder.name))
    proxy = os.environ.get('http_proxy', None)

    # Images defined by data uri schemas can be resolved into generated images
    # after a document's post-transformation stage. After a document's doctree
    # has been resolved, re-check for any images that have been translated.
    def assetsDocTreeResolvedHook(app, doctree, docname):
        if isinstance(app.builder, ConfluenceBuilder):
            app.builder.assets.processDocument(doctree, docname, True)
    app.connect('doctree-resolved', assetsDocTreeResolvedHook)

    """(essential)"""
    """Enablement of publishing."""
    app.add_config_value('confluence_publish', None, False)
    """API key/password to login to Confluence API with."""
    app.add_config_value('confluence_server_pass', None, False)
    """Username to login to Confluence API with."""
    app.add_config_value('confluence_server_user', None, False)
    """URL of the Confluence instance to publish to."""
    app.add_config_value('confluence_server_url', None, False)
    """Confluence Space to publish to."""
    app.add_config_value('confluence_space_name', None, False)

    """(generic)"""
    """Explicitly prevent page notifications on update."""
    app.add_config_value('confluence_disable_notifications', None, False)
    """File to get page header information from."""
    app.add_config_value('confluence_header_file', None, False)
    """File to get page footer information from."""
    app.add_config_value('confluence_footer_file', None, False)
    """Enablement of configuring master as space's homepage."""
    app.add_config_value('confluence_master_homepage', None, False)
    """Enablement of the maximum document depth (before inlining)."""
    app.add_config_value('confluence_max_doc_depth', None, False)
    """Enablement of publishing pages into a hierarchy from a master toctree."""
    app.add_config_value('confluence_page_hierarchy', None, False)
    """Root/parent page's name to publish documents into."""
    app.add_config_value('confluence_parent_page', None, False)
    """Show previous/next buttons (bottom, top, both, None)."""
    app.add_config_value('confluence_prev_next_buttons_location', None, False)
    """Postfix to apply to title of published pages."""
    app.add_config_value('confluence_publish_postfix', None, False)
    """Prefix to apply to published pages."""
    app.add_config_value('confluence_publish_prefix', None, False)
    """Enablement of purging legacy child pages from a parent page."""
    app.add_config_value('confluence_purge', None, False)
    """Enablement of purging legacy child pages from a master page."""
    app.add_config_value('confluence_purge_from_master', None, False)

    """(advanced-configuration - authentication)"""
    """Authentication passthrough for Confluence REST interaction."""
    app.add_config_value('confluence_server_auth', None, False)
    """Cookie(s) to use for Confluence REST interaction."""
    app.add_config_value('confluence_server_cookies', None, False)

    """(advanced-configuration - processing)"""
    """Filename suffix for generated files."""
    app.add_config_value('confluence_file_suffix', ".conf", False)
    """Translation of docname to a filename."""
    app.add_config_value('confluence_file_transform', None, False)
    """Indent to use for generated documents."""
    app.add_config_value('confluence_indent', STDINDENT, False)
    """Translation of a raw language to code block macro language."""
    app.add_config_value('confluence_lang_transform', None, False)
    """Link suffix for generated files."""
    app.add_config_value('confluence_link_suffix', None, False)
    """Translation of docname to a (partial) URI."""
    app.add_config_value('confluence_link_transform', None, False)
    """Remove a detected title from generated documents."""
    app.add_config_value('confluence_remove_title', True, False)

    """(advanced-configuration - publishing)"""
    """Request for publish username to come from interactive session."""
    app.add_config_value('confluence_ask_user', False, False)
    """Request for publish password to come from interactive session."""
    app.add_config_value('confluence_ask_password', False, False)
    """File/path to Certificate Authority"""
    """Tri-state asset handling (auto, force push or disable)."""
    app.add_config_value('confluence_asset_override', None, False)
    """File/path to Certificate Authority"""
    app.add_config_value('confluence_ca_cert', None, False)
    """Path to client certificate to use for publishing"""
    app.add_config_value('confluence_client_cert', None, False)
    """Password for client certificate to use for publishing"""
    app.add_config_value('confluence_client_cert_pass', None, False)
    """Explicitly prevent auto-generation of titles for titleless documents."""
    app.add_config_value('confluence_disable_autogen_title', None, False)
    """Explicitly prevent any Confluence REST API callers."""
    app.add_config_value('confluence_disable_rest', None, False)
    """Disable SSL validation with Confluence server."""
    app.add_config_value('confluence_disable_ssl_validation', None, False)
    """Explicitly prevent any Confluence XML-RPC API callers."""
    app.add_config_value('confluence_disable_xmlrpc', None, False)
    """Root/parent page's identifier to publish documents into."""
    app.add_config_value('confluence_parent_page_id_check', None, False)
    """Proxy server needed to communicate with Confluence server."""
    app.add_config_value('confluence_proxy', None, False)
    """Subset of document names to publish"""
    app.add_config_value('confluence_publish_subset', [], False)
    """Timeout for network-related calls (publishing)."""
    app.add_config_value('confluence_timeout', None, False)
    """Configuration for named JIRA Servers"""
    app.add_config_value('confluence_jira_servers', {}, True)

    """(advanced - undocumented)"""
    """Enablement for aggressive descendents search (for purge)."""
    app.add_config_value('confluence_adv_aggressive_search', None, False)
    """Enablement of the children macro for hierarchy mode."""
    app.add_config_value('confluence_adv_hierarchy_child_macro', None, False)
    """List of node types to ignore if no translator support exists."""
    app.add_config_value('confluence_adv_ignore_nodes', [], False)
    """List of extension-provided macros restricted for use."""
    app.add_config_value('confluence_adv_restricted_macros', [], False)
    """Enablement of tracing processed data."""
    app.add_config_value('confluence_adv_trace_data', False, False)
    """Do not cap sections to a maximum of six (6) levels."""
    app.add_config_value('confluence_adv_writer_no_section_cap', None, False)

    """JIRA directives"""
    """Adds the custom nodes needed for JIRA directives"""
    if not ConfluenceUtil.is_node_registered(jira):
        app.add_node(jira)
    if not ConfluenceUtil.is_node_registered(jira_issue):
        app.add_node(jira_issue)
    """Wires up the directives themselves"""
    app.add_directive('jira', JiraDirective)
    app.add_directive('jira_issue', JiraIssueDirective)

    if 'sphinx.ext.autosummary' in app.config.extensions:
        add_autosummary_nodes(app)

    # lazy bind sphinx.ext.imgmath to provide configuration options
    #
    # If 'sphinx.ext.imgmath' is not already explicitly loaded, bind it into the
    # setup process to a configurer can use the same configuration options
    # outlined in the sphinx.ext.imgmath in this extension. This applies for
    # Sphinx 1.8 and higher which math support is embedded; for older versions,
    # users will need to explicitly load 'sphinx.ext.mathbase'.
    if (imgmath is not None and
            'sphinx.ext.imgmath' not in app.config.extensions and
            parse_version(sphinx_version) >= parse_version('1.8')):
        imgmath.setup(app)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

def add_autosummary_nodes(app):
    """
    register custom nodes from autosummary extension

    The autosummary extensions adds custom nodes to the doctree.
    Add the required translation handlers manually.
    """
    app.registry.add_translation_handlers(
        autosummary.autosummary_table,
        confluence=(
            autosummary.autosummary_table_visit_html,
            autosummary.autosummary_noop)
    )
    app.registry.add_translation_handlers(
        autosummary.autosummary_toc,
        confluence=(
            autosummary.autosummary_toc_visit_html,
            autosummary.autosummary_noop)
    )
