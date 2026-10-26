# Limitations and dual-use (running list for the required appendix)

## Limitations

- **Prompt-conditioned behavior.** Payoffs are stated in prompts. Results describe how one
  model behaves under role instructions, not learned objectives or equilibrium strategies.
- **One model, one weekend.** Single small model; one to three seeds per cell; synthetic
  cases in one fictional domain. External validity is untested.
- **Regime labels mark opportunity, not verified coordination.** E1 label = incentive plus
  channel. The error analysis reports how often coordination was actually proposed and followed.
- **Payoff knowledge identifies the regime (CF-13).** Full S4 is reported only as an upper
  bound; the preregistered slice S4d has no payoff input. The matched channel-off trajectory
  (f10) is also unavailable to a deployer; an ablation removes it.
- **E1 and E0 proposer prompts differ by the channel note**, so presented evidence sets may
  differ between the pair. This is part of the treatment, but the error analysis reports the
  rate of presented-set differences. F and A share a byte-identical proposer prompt.
- **Rule features for text (f3, f9) are keyword-based** and will miss paraphrased plans.
  The LLM judge is the complement, with its own biases.
- **Approval criterion** uses ground truth; a deployer does not have it at decision time.
  The auditor is post hoc by design.
- **Scripted positive control is certain by construction**; it proves the pipeline, not
  that LLM coalitions behave the same way.

## Dual use

- A list of plus factors that auditors use is also a list of what a coalition should avoid
  producing. We judge this acceptable because the features are structural (provenance,
  exposure order, incentives) and already known in antitrust practice; concealing them
  would require changing the environment, not the messages.
- The colluding-proposer script is a two-line coordination message. It adds no capability
  beyond what the sprint's own starter repositories contain.
- No real organizations, people, or markets are modeled. All cases are fictional.
