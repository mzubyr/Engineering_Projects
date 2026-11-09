# Technical Notes: Magnetic Suspension MPC/PID Project

## Source

All historical values in this note are transcribed from `Thesis/Original_Bachelor_Thesis.pdf`, particularly Chapter 4, printed pages 19–23.

## Linearised model

The thesis gives:

\[
A = \begin{bmatrix}
0 & 1 & 0\\
196.2 & -0.01 & -3.1312\\
0 & 12.5284 & -40
\end{bmatrix},\quad
B = \begin{bmatrix}0\\0\\40\end{bmatrix}
\]

\[
C = \begin{bmatrix}1 & 0 & 0\end{bmatrix},\quad D=0
\]

and

\[
G(s)=\frac{-125.3}{s^3+40.01s^2-156.6s-7848}.
\]

The thesis describes the states as position, velocity and coil current. The manipulated input is voltage and the measured output is position.

## Original controller settings

The MPC table gives prediction horizon 29, control horizon 4 and sampling time 0.0064 s.

The PID table's proportional entry is printed as `-152`. The integral and derivative entries are printed as `-190` and `-16`.

## Original performance table

| Metric | PID | MPC |
|---|---:|---:|
| Rise time (s) | 0.0284 | 0.2374 |
| Settling time (s) | 1.2646 | 0.4051 |
| Peak time (s) | 0.0925 | 0.5568 |
| Maximum overshoot (%) | 74.300 | 0.5519 |

The thesis discussion says MPC improved settling time and overshoot, while PID had the faster rise time.

## Important provenance note

These are historical thesis results. They are not results from the later reconstruction. Any later simulation must be recorded separately with its own model, solver, sample time, controller configuration and measured performance.
