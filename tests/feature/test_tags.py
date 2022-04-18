"""Test tags."""
import textwrap

import pkg_resources
import pytest

from pytest_bdd.utils import get_tags


def test_tags_selector(testdir):
    """Test tests selection by tags."""
    testdir.makefile(
        ".ini",
        pytest=textwrap.dedent(
            """
    [pytest]
    markers =
        feature_tag_1
        feature_tag_2
        scenario_tag_01
        scenario_tag_02
        scenario_tag_10
        scenario_tag_20
    """
        ),
    )
    testdir.makefile(
        ".feature",
        test="""
    @feature_tag_1 @feature_tag_2
    Feature: Tags

    @scenario_tag_01 @scenario_tag_02
    Scenario: Tags
        Given I have a bar

    @scenario_tag_10 @scenario_tag_20
    Scenario: Tags 2
        Given I have a bar

    """,
    )
    testdir.makepyfile(
        """
        import pytest
        from pytest_bdd import given, scenarios

        @given('I have a bar')
        def i_have_bar():
            return 'bar'

        scenarios('test.feature')
    """
    )
    result = testdir.runpytest("-m", "scenario_tag_10 and not scenario_tag_01", "-vv")
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 1

    result = testdir.runpytest("-m", "scenario_tag_01 and not scenario_tag_10", "-vv").parseoutcomes()
    assert result["passed"] == 1
    assert result["deselected"] == 1

    result = testdir.runpytest("-m", "feature_tag_1", "-vv").parseoutcomes()
    assert result["passed"] == 2

    result = testdir.runpytest("-m", "feature_tag_10", "-vv").parseoutcomes()
    assert result["deselected"] == 2


# TODO adapt test for old parser
# def test_tags_selector_with_examples(testdir):
#     """Test tests selection by tags."""
#     testdir.makefile(
#         ".ini",
#         pytest=textwrap.dedent(
#             """\
#                 [pytest]
#                 markers =
#                     feature_tag_1
#                     feature_tag_2
#                     background_example_tag_01
#                     background_example_tag_02
#                     background_example_tag_03
#                     background_example_tag_04
#                     scenario_tag_01
#                     scenario_tag_02
#                     scenario_tag_10
#                     scenario_tag_20
#                     scenario_example_tag_01
#                     scenario_example_tag_02
#                     scenario_example_tag_03
#                     scenario_example_tag_04
#                 """
#         ),
#     )
#     testdir.makefile(
#         ".feature",
#         test=textwrap.dedent(
#             """\
#         @feature_tag_1 @feature_tag_2
#         Feature: Tags
#             Background:
#                 Given I have an <background_example> for background
#
#                 @background_example_tag_01
#                 Examples: Nice background example
#                   |background_example|
#                   |        1         |
#
#                 @background_example_tag_02
#                 Examples:
#                   |background_example|
#                   |        2         |
#
#                 @background_example_tag_03
#                 Examples: Vertical
#                   |background_example| 3 |
#
#                 @background_example_tag_04
#                 Examples: Vertical Another example
#                   |background_example| 4 |
#
#             @scenario_tag_01 @scenario_tag_02
#             Scenario: Tags
#                 Given I have a bar
#
#             @scenario_tag_10 @scenario_tag_20
#             Scenario: Tags 2
#                 Given I have a bar
#                 Given I have an <scenario_example> for scenario
#
#                 @scenario_example_tag_01
#                 Examples:
#                   |scenario_example|
#                   |        5       |
#
#                 @scenario_example_tag_02
#                 Examples:
#                   |scenario_example|
#                   |        6       |
#                 @scenario_example_tag_03
#                 Examples: Vertical Scenario example
#                   |scenario_example| 7 |
#
#                 @scenario_example_tag_04
#                 Examples: Vertical
#                   |scenario_example| 8 |
#         """,
#         ),
#     )
#     testdir.makepyfile(
#         textwrap.dedent(
#             """\
#         import pytest
#         from pytest_bdd import given, scenarios
#
#         @given('I have a bar')
#         def i_have_bar():
#             return 'bar'
#
#         @given('I have an {example} for background')
#         def i_have_bar(example):
#             return example
#
#         @given('I have an {example} for scenario')
#         def i_have_bar(example):
#             return example
#
#         scenarios('test.feature')
#         """
#         )
#     )
#
#     result = testdir.runpytest("-m", "scenario_tag_10 and not scenario_tag_01", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 16
#     assert outcomes["deselected"] == 4
#
#     result = testdir.runpytest("-m", "scenario_tag_01 and not scenario_tag_10", "-vv").parseoutcomes()
#     assert result["passed"] == 4
#     assert result["deselected"] == 16
#
#     result = testdir.runpytest("-m", "feature_tag_1", "-vv").parseoutcomes()
#     assert result["passed"] == 20
#
#     result = testdir.runpytest("-m", "feature_tag_10", "-vv").parseoutcomes()
#     assert result["deselected"] == 20
#
#     result = testdir.runpytest("-m", "scenario_example_tag_01", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 4
#     assert outcomes["deselected"] == 16
#
#     result = testdir.runpytest("-m", "background_example_tag_01 and scenario_example_tag_01", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 1
#     assert outcomes["deselected"] == 19
#
#     result = testdir.runpytest("-m", "background_example_tag_01 and scenario_tag_10", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 4
#     assert outcomes["deselected"] == 16


# TODO: adapt test for old parser
# def test_tags_selector_with_empty_examples(testdir):
#     """Test tests selection by tags."""
#     testdir.makefile(
#         ".ini",
#         pytest=textwrap.dedent(
#             """\
#                 [pytest]
#                 markers =
#                     feature_tag
#                     background_example_tag
#                     scenario_tag
#                     scenario_example_tag
#                 """
#         ),
#     )
#     testdir.makefile(
#         ".feature",
#         test=textwrap.dedent(
#             """\
#         @feature_tag
#         Feature: Tags
#             Background:
#                 Given I have <background_example>
#
#                 @background_example_tag
#                 Examples: Nice background example
#                   |background_example|
#                   |        1         |
#
#
#             @scenario_tag
#             Scenario: Tags
#                 Given I have a bar
#
#                 @scenario_example_tag
#                 Examples:
#                   |
#         """,
#         ),
#     )
#     testdir.makepyfile(
#         textwrap.dedent(
#             """\
#         import pytest
#         from pytest_bdd import given, scenarios
#
#         @given('I have a bar')
#         def i_have_bar():
#             return 'bar'
#
#         @given('I have {background_example:d}')
#         def i_have_bar(background_example):
#             return background_example
#
#         scenarios('test.feature')
#         """
#         )
#     )
#
#     result = testdir.runpytest("-m", "scenario_example_tag", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 1

# TODO adapt test for old parser
# def test_tags_selector_with_inlined_tags_examples(testdir):
#     """Test tests selection by tags in examples rows."""
#     testdir.makefile(
#         ".ini",
#         pytest=textwrap.dedent(
#             """\
#                 [pytest]
#                 markers =
#                     background_example_tag_01
#                     background_example_tag_02
#                     background_example_tag_03
#                     background_example_tag_04
#                     scenario_tag_01
#                     scenario_tag_02
#                     scenario_tag_10
#                     scenario_tag_20
#                     scenario_example_tag_01
#                     scenario_example_tag_02
#                     scenario_example_tag_03
#                     scenario_example_tag_04
#                 """
#         ),
#     )
#     testdir.makefile(
#         ".feature",
#         test=textwrap.dedent(
#             """\
#                 Feature: Tags
#                     Background:
#                         Given I have an <background_example> for background
#
#                         Examples: Nice background example
#                           | background_example | @                         | @                         |
#                           |         1          | background_example_tag_01 | background_example_tag_04 |
#
#                         Examples:
#                           | background_example | @                         |
#                           |         2          | background_example_tag_02 |
#
#                         Examples: Vertical
#                           | background_example | 3                         |
#                           | @                  | background_example_tag_03 |
#
#                         Examples: Vertical Another example
#                           | background_example | 4                         |
#                           | @                  | background_example_tag_04 |
#
#                     @scenario_tag_01 @scenario_tag_02
#                     Scenario: Tags
#                         Given I have a bar
#
#                     @scenario_tag_10 @scenario_tag_20
#                     Scenario: Tags 2
#                         Given I have a bar
#                         Given I have an <scenario_example> for scenario
#
#                         @scenario_example_tag_01
#                         Examples:
#                           |scenario_example|
#                           |        5       |
#
#                         Examples:
#                           |scenario_example| @                       |
#                           |        6       | scenario_example_tag_02 |
#
#                         Examples: Vertical Scenario example
#                           | scenario_example | 7                       |
#                           | @                | scenario_example_tag_03 |
#                           | @                | scenario_example_tag_04 |
#
#                         @scenario_example_tag_04
#                         Examples: Vertical
#                           | scenario_example | 8 |
#                 """,
#         ),
#     )
#     testdir.makepyfile(
#         textwrap.dedent(
#             """\
#         import pytest
#         from pytest_bdd import given, scenarios
#
#         @given('I have a bar')
#         def i_have_bar():
#             return 'bar'
#
#         @given('I have an {example} for background')
#         def i_have_bar(example):
#             return example
#
#         @given('I have an {example} for scenario')
#         def i_have_bar(example):
#             return example
#
#         scenarios('test.feature')
#         """
#         )
#     )
#
#     result = testdir.runpytest("-m", "scenario_example_tag_01", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 4
#     assert outcomes["deselected"] == 16
#
#     result = testdir.runpytest(
#         "-m", "scenario_example_tag_03 and scenario_example_tag_04 and not background_example_tag_02", "-vv"
#     )
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 3
#     assert outcomes["deselected"] == 17
#
#     result = testdir.runpytest("-m", "background_example_tag_01 and scenario_example_tag_01", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 1
#     assert outcomes["deselected"] == 19
#
#     result = testdir.runpytest(
#         "-m", "background_example_tag_01 and not background_example_tag_04 and scenario_example_tag_01", "-vv"
#     )
#     outcomes = result.parseoutcomes()
#     assert outcomes["deselected"] == 20
#
#     result = testdir.runpytest("-m", "background_example_tag_01 and scenario_tag_10", "-vv")
#     outcomes = result.parseoutcomes()
#     assert outcomes["passed"] == 4
#     assert outcomes["deselected"] == 16


def test_tags_after_background_issue_160(testdir):
    """Make sure using a tag after background works."""
    testdir.makefile(
        ".ini",
        pytest=textwrap.dedent(
            """
    [pytest]
    markers = tag
    """
        ),
    )
    testdir.makefile(
        ".feature",
        test="""
    Feature: Tags after background

        Background:
            Given I have a bar

        @tag
        Scenario: Tags
            Given I have a baz

        Scenario: Tags 2
            Given I have a baz
    """,
    )
    testdir.makepyfile(
        """
        import pytest
        from pytest_bdd import given, scenarios

        @given('I have a bar')
        def i_have_bar():
            return 'bar'

        @given('I have a baz')
        def i_have_baz():
            return 'baz'

        scenarios('test.feature')
    """
    )
    result = testdir.runpytest("-m", "tag", "-vv").parseoutcomes()
    assert result["passed"] == 1
    assert result["deselected"] == 1


# TODO adapt test for old parser
# def test_tag_with_spaces(testdir):
#     testdir.makefile(
#         ".ini",
#         pytest=textwrap.dedent(
#             """
#     [pytest]
#     markers =
#         test with spaces
#     """
#         ),
#     )
#     testdir.makeconftest(
#         """
#         import pytest
#
#         @pytest.hookimpl(tryfirst=True)
#         def pytest_bdd_apply_tag(tag, function):
#             assert tag == 'test with spaces'
#     """
#     )
#     testdir.makefile(
#         ".feature",
#         test="""
#     Feature: Tag with spaces
#
#         @test with spaces
#         Scenario: Tags
#             Given I have a bar
#     """,
#     )
#     testdir.makepyfile(
#         """
#         from pytest_bdd import given, scenarios
#
#         @given('I have a bar')
#         def i_have_bar():
#             return 'bar'
#
#         scenarios('test.feature')
#     """
#     )
#     result = testdir.runpytest_subprocess()
#     result.stdout.fnmatch_lines(["*= 1 passed * =*"])


def test_at_in_scenario(testdir):
    testdir.makefile(
        ".feature",
        test="""
    Feature: At sign in a scenario

        Scenario: Tags
            Given I have a foo@bar

        Scenario: Second
            Given I have a baz
    """,
    )
    testdir.makepyfile(
        """
        from pytest_bdd import given, scenarios

        @given('I have a foo@bar')
        def i_have_at():
            return 'foo@bar'

        @given('I have a baz')
        def i_have_baz():
            return 'baz'

        scenarios('test.feature')
    """
    )

    # Deprecate --strict after pytest 6.1
    # https://docs.pytest.org/en/stable/deprecations.html#the-strict-command-line-option
    pytest_version = pkg_resources.get_distribution("pytest").parsed_version
    if pytest_version >= pkg_resources.parse_version("6.2"):
        strict_option = "--strict-markers"
    else:
        strict_option = "--strict"
    result = testdir.runpytest_subprocess(strict_option)
    result.stdout.fnmatch_lines(["*= 2 passed * =*"])


@pytest.mark.parametrize(
    "line, expected",
    [
        ("@foo @bar", {"foo", "bar"}),
        ("@with spaces @bar", {"with spaces", "bar"}),
        ("@double @double", {"double"}),
        ("    @indented", {"indented"}),
        (None, set()),
        ("foobar", set()),
        ("", set()),
    ],
)
def test_get_tags(line, expected):
    assert get_tags(line) == expected


def test_invalid_tags(testdir):
    features = testdir.mkdir("features")
    features.join("test.feature").write_text(
        textwrap.dedent(
            """\
                Feature: Invalid tags
                    Scenario: Invalid tags
                        @tag
                        Given foo
                        When bar
                        Then baz
                """
        ),
        "utf-8",
        ensure=True,
    )
    testdir.makepyfile(
        textwrap.dedent(
            """\
                from pytest_bdd import scenarios

                scenarios('features')
                """
        )
    )
    result = testdir.runpytest()
    result.stdout.fnmatch_lines(["*FeatureError*"])
