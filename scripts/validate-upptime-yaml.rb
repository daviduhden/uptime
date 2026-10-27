#!/usr/bin/env ruby
# UPT001: Parse changed Upptime YAML with the runner's standard Psych library.

require "yaml"

paths = STDIN.read.split("\0").reject(&:empty?)
errors = []

paths.each do |path|
  next unless File.file?(path)

  begin
    YAML.safe_load(File.read(path), aliases: true)
  rescue Psych::Exception, SystemCallError => error
    errors << [path, error.message.lines.first&.strip || "invalid YAML"]
  end
end

if errors.empty?
  puts "[PASS] UPT001 - Changed YAML documents valid"
  exit 0
end

errors.each do |path, message|
  warn "[FAIL] UPT001 - Invalid YAML: #{path}"
  warn "  Detail: #{message}"
  warn "  Action: Correct the YAML syntax and rerun this check."
end
exit 1
