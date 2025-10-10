ROLE ?= architect
OWNER ?= TBD
SPRINT ?= S2_Automation_Foundation

brief:
	bin/haws-new-brief --role $(ROLE) --owner "$(OWNER)" --sprint "$(SPRINT)"

verify:
	@echo "OK: tooling targets present (brief/verify)"
