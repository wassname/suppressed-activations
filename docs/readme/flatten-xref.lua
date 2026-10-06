-- From wassname's quarto skill (resources/flatten-xref.lua), plus Span unwrapping. Post-pass on README.md.
-- Flatten quarto crossref + citeproc HTML to plain markdown.
-- Quarto emits crossrefs as RawInline html (<a class="quarto-xref">Table 3</a>)
-- and wraps floats / the bibliography in <div id="..."> RawBlocks. LessWrong's
-- markdown does not want the raw tags, so unwrap them: keep the visible text,
-- drop the div wrappers. Runs after crossref resolution, alongside strip-comments.lua.

-- commonmark_x renders @fig-/@tbl- crossrefs as reference-links [Figure 1](#fig-toy)
-- with a quarto-xref class. The #anchor is dead on LessWrong, so flatten to plain text.
function Link(el)
  for _, c in ipairs(el.classes) do
    if c == 'quarto-xref' then return el.content end
  end
  return el
end

function RawInline(el)
  if el.format:match('html') then
    -- whole anchor in one node: <a ... quarto-xref ...>Table 3</a> -> Table 3
    local txt = el.text:match('quarto%-xref"[^>]*>(.-)</a>')
    if txt then return pandoc.Str(txt) end
    -- split across nodes: drop the opening quarto-xref <a ...> and any closing </a>,
    -- leaving the visible "Table 3" / "Figure 1" text between them.
    if el.text:match('quarto%-xref') or el.text:match('^%s*</a>%s*$') then
      return {}
    end
    -- citeproc's <span class="nocase"> arrives as raw html when README.md is re-read
    if el.text:match('^<span class="nocase">$') or el.text:match('^</span>$') then
      return {}
    end
  end
  return el
end

function RawBlock(el)
  if el.format:match('html') then
    local t = el.text:gsub('%s+', '')
    if t:match('^<div') or t == '</div>' then
      return {}
    end
  end
  return el
end

-- citeproc wraps "et al." author strings in <span class="nocase">; keep the text only
function Span(el)
  return el.content
end
